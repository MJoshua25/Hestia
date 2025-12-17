from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Standard_model(models.Model):
	statut = models.BooleanField(default=True)
	date_add = models.DateTimeField(auto_now_add=True)
	date_upd = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True

class User(AbstractUser):

    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    pin_code = models.CharField(max_length=128, null=True, blank=True)  # Hashé avec make_password()
    require_password_change = models.BooleanField(default=True)

    def set_pin(self, pin):

        """Hash et stocke le code PIN"""
        from django.contrib.auth.hashers import make_password
        self.pin_code = make_password(pin)
        self.save()

    def check_pin(self, pin):
        """Vérifie le code PIN"""
        from django.contrib.auth.hashers import check_password
        return check_password(pin, self.pin_code)