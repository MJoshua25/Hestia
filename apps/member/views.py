import json
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView, View
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db import transaction
from .models import Member
from .forms import MemberForm, MemberFormSet, ProfileForm
from .services import MemberService
from core.mixins import AdminOrDelegateRequiredMixin
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

class MemberListView(LoginRequiredMixin, ListView):
    model = Member
    template_name = 'member/member_list.html'
    context_object_name = 'members'
    paginate_by = 20
    
    def get_queryset(self):
        # Start with base queryset
        queryset = Member.objects.all()
        
        # Filter by status (active by default)
        status = self.request.GET.get('status', 'active')
        if status == 'archived':
            queryset = queryset.filter(statut=False)
        else:
            queryset = queryset.filter(statut=True)
            
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(first_name__icontains=query) | 
                Q(last_name__icontains=query) |
                Q(room_number__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_count'] = Member.objects.filter(statut=True).count()
        context['archived_count'] = Member.objects.filter(statut=False).count()
        context['current_status'] = self.request.GET.get('status', 'active')
        return context

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

class ProfileView(LoginRequiredMixin, UpdateView):
    model = Member
    form_class = ProfileForm
    template_name = 'member/profile.html'
    success_url = reverse_lazy('member:profile')

    def get_object(self, queryset=None):
        return self.request.user.member_profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['password_form'] = PasswordChangeForm(self.request.user)
        # Stats context
        member = self.get_object()
        from apps.event.models import Assignment, Commission
        
        events_count = Assignment.objects.filter(member=member).count()
        commissions_count = Assignment.objects.filter(member=member).values('commission__event').distinct().count()
        responsibilities_count = Commission.objects.filter(responsible=member).count()
        last_participation = Assignment.objects.filter(member=member).order_by('-commission__event__date').first()
        
        context['stats'] = {
            'events_count': events_count,
            'commissions_count': commissions_count,
            'responsibilities_count': responsibilities_count,
            'last_participation': last_participation
        }
        return context

    def form_valid(self, form):
        messages.success(self.request, "Informations mises à jour avec succès")
        return super().form_valid(form)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Votre mot de passe a été mis à jour avec succès.')
            return redirect('member:profile')
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            return redirect('member:profile')
    return redirect('member:profile')

@login_required
def manage_pin(request):
    if request.method == 'POST':
        pin = request.POST.get('pin')
        confirm_pin = request.POST.get('confirm_pin')
        current_password = request.POST.get('password')
        
        if not request.user.check_password(current_password):
            return JsonResponse({'success': False, 'error': 'Mot de passe incorrect'})
            
        if pin != confirm_pin:
             return JsonResponse({'success': False, 'error': 'Les codes PIN ne correspondent pas'})
             
        if not pin.isdigit() or len(pin) != 6:
             return JsonResponse({'success': False, 'error': 'Le code PIN doit contenir 6 chiffres'})
             
        request.user.set_pin(pin)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Méthode non autorisée'})

@login_required
def delete_photo(request):
    if request.method == 'POST':
        member = request.user.member_profile
        if member.photo:
            member.photo.delete()
            member.save()
            messages.success(request, "Photo supprimée")
        return redirect('member:profile')
    return redirect('member:profile')

@login_required
def archive_member(request, pk):
    if not request.user.member_profile.is_admin:
        messages.error(request, "Action réservée aux administrateurs")
        return redirect('member:member_list')
        
    member = get_object_or_404(Member, pk=pk)
    if request.method == 'POST':
        # Deactivate user
        if member.user:
            member.user.is_active = False
            member.user.save()
            
        # Soft delete member
        member.statut = False
        member.save()
        
        # Remove from future commissions
        from django.utils import timezone
        from apps.event.models import Assignment
        
        Assignment.objects.filter(
            member=member,
            commission__event__date__gte=timezone.now()
        ).delete()
        
        messages.success(request, f"{member} archivé avec succès")
        return redirect('member:member_list')
    return redirect('member:member_list')

@login_required
def restore_member(request, pk):
    if not request.user.member_profile.is_admin:
        messages.error(request, "Action réservée aux administrateurs")
        return redirect('member:member_list')
        
    member = get_object_or_404(Member, pk=pk)
    if request.method == 'POST':
        # Reactivate user
        if member.user:
            member.user.is_active = True
            member.user.save()
            
        # Restore member
        member.statut = True
        member.save()
        
        messages.success(request, f"{member} restauré avec succès")
        return redirect('member:member_list')
    return redirect('member:member_list')

@login_required
def delete_member_permanently(request, pk):
    if not request.user.member_profile.is_admin:
        messages.error(request, "Action réservée aux administrateurs")
        return redirect('member:member_list')
        
    member = get_object_or_404(Member, pk=pk)
    if request.method == 'POST':
        if member.statut: # Should be archived first
            messages.error(request, "Le membre doit être archivé avant suppression définitive")
            return redirect('member:member_list')
            
        # Delete user
        if member.user:
            member.user.delete()
        else:
            member.delete()
            
        messages.success(request, f"{member} supprimé définitivement")
        return redirect('member:member_list')
    return redirect('member:member_list')
