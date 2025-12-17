from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from core.models import Standard_model

User = get_user_model()

class Member(Standard_model):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', _('Admin')
        DELEGATE = 'DELEGATE', _('Déléguée')
        MEMBER = 'MEMBER', _('Membre')

    user = models.OneToOneField(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='member_profile'
    )
    
    first_name = models.CharField(_('Prénom'), max_length=100)
    last_name = models.CharField(_('Nom'), max_length=100)
    
    # Simple regex validation for phone number for now, can be improved with phonenumbers lib
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', 
        message=_("Le numéro de téléphone doit être au format: '+999999999'. Jusqu'à 15 chiffres.")
    )
    phone_number = models.CharField(
        _('Numéro de téléphone'), 
        validators=[phone_regex], 
        max_length=17, 
        unique=True
    )
    
    room_number = models.CharField(_('Chambre'), max_length=20)
    
    role = models.CharField(
        _('Rôle'), 
        max_length=20, 
        choices=Role.choices, 
        default=Role.MEMBER
    )

    class Meta:
        verbose_name = _('Membre')
        verbose_name_plural = _('Membres')
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN

    @property
    def is_delegate(self):
        return self.role == self.Role.DELEGATE
