from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.member.models import Member
from apps.event.models import Event, Commission
from django.utils import timezone

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        try:
            member = user.member_profile
        except Member.DoesNotExist:
            member = None
        
        context['member'] = member
        now = timezone.now()

        if member and (member.is_admin or member.is_delegate):
            # Admin/Delegate Dashboard
            context['total_members'] = Member.objects.filter(statut=True).count()
            context['upcoming_events_count'] = Event.objects.filter(date__gte=now).count()
            context['active_commissions_count'] = Commission.objects.filter(event__date__gte=now).count()
            
            context['upcoming_events'] = Event.objects.filter(date__gte=now).order_by('date')[:5]
            
        elif member:
            # Member Dashboard
            # My commissions
            context['my_commissions'] = member.commissions.filter(event__date__gte=now).select_related('event')
            
        return context
