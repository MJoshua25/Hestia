from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404, redirect
from .models import Event, Commission
from .forms import EventForm, CommissionForm
from apps.member.models import Member

class AdminOrDelegateRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        if not self.request.user.is_authenticated:
            return False
        try:
            member = self.request.user.member_profile
            return member.is_admin or member.is_delegate
        except Member.DoesNotExist:
            return False

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        if not self.request.user.is_authenticated:
            return False
        try:
            member = self.request.user.member_profile
            return member.is_admin
        except Member.DoesNotExist:
            return False

class EventListView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'event/event_list.html'
    context_object_name = 'events'
    paginate_by = 20

    def get_queryset(self):
        return Event.objects.all().order_by('date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Separate past and future events?
        # PRD says: "voir deux sections : Événements à venir et Événements passés"
        # But ListView usually iterates over one list.
        # I can split them in template or context.
        from django.utils import timezone
        now = timezone.now()
        context['upcoming_events'] = Event.objects.filter(date__gte=now).order_by('date')
        context['past_events'] = Event.objects.filter(date__lt=now).order_by('-date')
        context['undated_events'] = Event.objects.filter(date__isnull=True)
        return context

class EventDetailView(LoginRequiredMixin, DetailView):
    model = Event
    template_name = 'event/event_detail.html'
    context_object_name = 'event'

class EventCreateView(AdminOrDelegateRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'event/event_form.html'
    
    def get_success_url(self):
        return reverse('event_detail', kwargs={'pk': self.object.pk})

class EventUpdateView(AdminOrDelegateRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'event/event_form.html'
    
    def get_success_url(self):
        return reverse('event_detail', kwargs={'pk': self.object.pk})

class EventDeleteView(AdminRequiredMixin, DeleteView):
    model = Event
    template_name = 'event/event_confirm_delete.html'
    success_url = reverse_lazy('event_list')

# Commission Management
class CommissionCreateView(AdminOrDelegateRequiredMixin, CreateView):
    model = Commission
    form_class = CommissionForm
    template_name = 'event/commission_form.html'

    def form_valid(self, form):
        event = get_object_or_404(Event, pk=self.kwargs['event_id'])
        form.instance.event = event
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('event_detail', kwargs={'pk': self.kwargs['event_id']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = get_object_or_404(Event, pk=self.kwargs['event_id'])
        return context

class CommissionUpdateView(AdminOrDelegateRequiredMixin, UpdateView):
    model = Commission
    form_class = CommissionForm
    template_name = 'event/commission_form.html'

    def get_success_url(self):
        return reverse('event_detail', kwargs={'pk': self.object.event.pk})

class CommissionDeleteView(AdminOrDelegateRequiredMixin, DeleteView):
    model = Commission
    template_name = 'event/commission_confirm_delete.html'
    
    def get_success_url(self):
        return reverse('event_detail', kwargs={'pk': self.object.event.pk})
