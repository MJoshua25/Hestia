from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import Standard_model
from apps.member.models import Member

class Event(Standard_model):
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', _('Brouillon')
        PUBLISHED = 'PUBLISHED', _('Publié')

    title = models.CharField(_('Titre'), max_length=200)
    description = models.TextField(_('Description'), blank=True)
    date = models.DateTimeField(_('Date'), null=True, blank=True, db_index=True)
    location = models.CharField(_('Lieu'), max_length=200, blank=True)
    
    status = models.CharField(
        _('Statut'), 
        max_length=20, 
        choices=Status.choices, 
        default=Status.PUBLISHED
    )

    class Meta:
        verbose_name = _('Événement')
        verbose_name_plural = _('Événements')
        ordering = ['date']

    def __str__(self):
        return self.title

class Commission(Standard_model):
    event = models.ForeignKey(
        Event, 
        on_delete=models.CASCADE, 
        related_name='commissions',
        verbose_name=_('Événement')
    )
    name = models.CharField(_('Nom'), max_length=100)
    description = models.TextField(_('Description'), blank=True)
    max_capacity = models.PositiveIntegerField(_('Capacité max'), default=5)
    members = models.ManyToManyField(
        Member, 
        related_name='commissions', 
        blank=True,
        verbose_name=_('Membres assignés')
    )

    class Meta:
        verbose_name = _('Commission')
        verbose_name_plural = _('Commissions')

    def __str__(self):
        return f"{self.name} ({self.event.title})"
