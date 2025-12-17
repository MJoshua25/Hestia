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
    min_capacity = models.PositiveIntegerField(_('Capacité min'), default=0)
    max_capacity = models.PositiveIntegerField(_('Capacité max'), null=True, blank=True, help_text=_("Laisser vide pour illimité"))
    responsible = models.ForeignKey(
        Member, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='responsible_commissions',
        verbose_name=_('Responsable')
    )

    class Meta:
        verbose_name = _('Commission')
        verbose_name_plural = _('Commissions')

    def __str__(self):
        return f"{self.name} ({self.event.title})"
    
    @property
    def current_count(self):
        return self.assignments.count()
    
    @property
    def is_full(self):
        if self.max_capacity is None:
            return False
        return self.current_count >= self.max_capacity

class Assignment(Standard_model):
    commission = models.ForeignKey(
        Commission, 
        on_delete=models.CASCADE, 
        related_name='assignments',
        verbose_name=_('Commission')
    )
    member = models.ForeignKey(
        Member, 
        on_delete=models.CASCADE, 
        related_name='assignments',
        verbose_name=_('Membre')
    )
    assigned_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Assigné le'))
    assigned_by = models.ForeignKey(
        'core.User', 
        on_delete=models.SET_NULL, 
        null=True, 
        verbose_name=_('Assigné par')
    )

    class Meta:
        verbose_name = _('Attribution')
        verbose_name_plural = _('Attributions')
        unique_together = [['commission', 'member']]

    def __str__(self):
        return f"{self.member} -> {self.commission}"
