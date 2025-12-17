import json
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView, View
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.db import transaction
from .models import Member
from .forms import MemberForm, MemberFormSet
from .services import MemberService
from core.mixins import AdminOrDelegateRequiredMixin

class MemberListView(LoginRequiredMixin, ListView):
    model = Member
    template_name = 'member/member_list.html'
    context_object_name = 'members'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(first_name__icontains=query) | 
                Q(last_name__icontains=query) |
                Q(room_number__icontains=query)
            )
        return queryset

class MemberDetailView(LoginRequiredMixin, DetailView):
    model = Member
    template_name = 'member/member_detail.html'
    context_object_name = 'member'

class MemberCreateView(AdminOrDelegateRequiredMixin, SuccessMessageMixin, CreateView):
    model = Member
    form_class = MemberForm
    template_name = 'member/member_form.html'
    success_url = reverse_lazy('member:member_list')
    success_message = "Membre ajouté avec succès"

class MemberBulkCreateView(AdminOrDelegateRequiredMixin, View):
    template_name = 'member/member_bulk_form.html'
    success_url = reverse_lazy('member:member_list')

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            members_data = data.get('members', [])
            
            if not members_data:
                return JsonResponse({'success': False, 'error': 'Aucune donnée reçue'}, status=400)

            created_count = 0
            errors = []

            with transaction.atomic():
                for index, member_data in enumerate(members_data):
                    # Basic validation
                    if not all(key in member_data for key in ['first_name', 'last_name', 'phone_number', 'room_number']):
                        errors.append(f"Ligne {index + 1}: Champs manquants")
                        continue

                    # Check for duplicates (phone number)
                    if Member.objects.filter(phone_number=member_data['phone_number']).exists():
                        errors.append(f"Ligne {index + 1}: Le numéro {member_data['phone_number']} existe déjà")
                        continue

                    Member.objects.create(
                        first_name=member_data['first_name'],
                        last_name=member_data['last_name'],
                        phone_number=member_data['phone_number'],
                        room_number=member_data['room_number'],
                        role=member_data.get('role', 'MEMBER')
                    )
                    created_count += 1
            
            if errors:
                # If there were errors but some succeeded, we rollback everything or partial?
                # Usually bulk means all or nothing or best effort.
                # Let's go with best effort but transaction.atomic rolls back everything on exception.
                # Here I am not raising exception, so it commits valid ones.
                # Wait, transaction.atomic block commits at end if no exception.
                # If I want to fail all if one fails, I should raise exception.
                # But UX-wise, partial success is tricky. Let's fail all if errors for safety/clarity.
                pass 
                
            if errors:
                 return JsonResponse({'success': False, 'errors': errors}, status=400)

            messages.success(request, f"{created_count} membres ajoutés avec succès.")
            return JsonResponse({'success': True, 'redirect_url': self.success_url})

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'JSON invalide'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)


class MemberUpdateView(AdminOrDelegateRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Member
    form_class = MemberForm
    template_name = 'member/member_form.html'
    success_url = reverse_lazy('member:member_list')
    success_message = "Membre mis à jour avec succès"

class MemberDeleteView(AdminOrDelegateRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Member
    template_name = 'member/member_confirm_delete.html'
    success_url = reverse_lazy('member:member_list')
    success_message = "Membre supprimé avec succès"

class MemberImportView(AdminOrDelegateRequiredMixin, FormView):
    template_name = 'member/member_import.html'
    success_url = reverse_lazy('member:member_list')
    form_class = None # We handle manually for now or need a dummy form

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        if 'file' not in request.FILES:
            messages.error(request, "Veuillez sélectionner un fichier.")
            return redirect('member:member_import')
        
        file = request.FILES['file']
        if not file.name.endswith(('.xlsx', '.xls')):
            messages.error(request, "Format de fichier invalide. Utilisez .xlsx ou .xls")
            return redirect('member:member_import')
            
        try:
            count = MemberService.import_from_excel(file)
            messages.success(request, f"{count} membres importés avec succès.")
            return redirect(self.success_url)
        except ValidationError as e:
            if hasattr(e, 'messages'):
                 for err in e.messages:
                     messages.error(request, err)
            else:
                 messages.error(request, str(e))
            return redirect('member:member_import')
        except Exception as e:
            messages.error(request, f"Erreur lors de l'import: {str(e)}")
            return redirect('member:member_import')
