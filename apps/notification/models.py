from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class Notification(models.Model):
    class Type(models.TextChoices):
        ASSIGNMENT = 'ASSIGNMENT', _('Attribution')
        EVENT = 'EVENT', _('Événement')
        MODIFICATION = 'MODIFICATION', _('Modification')
        COMMISSION = 'COMMISSION', _('Commission')
        SYSTEM = 'SYSTEM', _('Système')

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name=_('Utilisateur')
    )
    
    type = models.CharField(
        _('Type'),
        max_length=20,
        choices=Type.choices,
        default=Type.SYSTEM
    )
    
    title = models.CharField(_('Titre'), max_length=255)
    message = models.TextField(_('Message'))
    link = models.CharField(_('Lien'), max_length=255, blank=True)
    
    is_read = models.BooleanField(_('Lu'), default=False)
    created_at = models.DateTimeField(_('Créé le'), auto_now_add=True)

    class Meta:
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.type} - {self.user} - {self.title}"

    @property
    def icon(self):
        icons = {
            self.Type.ASSIGNMENT: '📋',
            self.Type.EVENT: '📅',
            self.Type.MODIFICATION: '✏️',
            self.Type.COMMISSION: '🔄',
            self.Type.SYSTEM: '📢',
        }
        return icons.get(self.type, '🔔')
