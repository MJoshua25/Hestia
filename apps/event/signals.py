from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext as _
from django.urls import reverse
from .models import Event
from apps.notification.services import NotificationService
from apps.notification.models import Notification

@receiver(post_save, sender=Event)
def notify_event_changes(sender, instance, created, **kwargs):
    """
    Notify members about new events or modifications.
    """
    if created:
        # Notify ALL active members about new event
        # We need to import Member here to avoid circular import if possible, 
        # but signals are usually loaded at startup.
        from apps.member.models import Member
        
        # Get all users linked to active members
        members = Member.objects.filter(statut=True, user__isnull=False).select_related('user')
        users = [m.user for m in members]
        
        NotificationService.create_bulk_notifications(
            users=users,
            type=Notification.Type.EVENT,
            title=_("Nouvel événement !"),
            message=f"{instance.title} - {instance.date.strftime('%d/%m/%Y')}",
            link=reverse('event_detail', args=[instance.id])
        )
    else:
        # Notify only assigned members about modification
        # Get members assigned to any commission of this event
        from apps.member.models import Member
        
        assigned_members = Member.objects.filter(
            assignments__commission__event=instance,
            user__isnull=False
        ).distinct().select_related('user')
        
        users = [m.user for m in assigned_members]
        
        if users:
            NotificationService.create_bulk_notifications(
                users=users,
                type=Notification.Type.MODIFICATION,
                title=_("Événement modifié"),
                message=_("{} : L'événement a été modifié.").format(instance.title),
                link=reverse('event_detail', args=[instance.id])
            )
