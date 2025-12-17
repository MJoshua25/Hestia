from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class PhonePasswordBackend(ModelBackend):
    """Authentification par numéro + password"""
    def authenticate(self, request, phone_number=None, password=None, **kwargs):
        if phone_number is None:
            return None
        try:
            # Nettoyage basique du numéro si besoin, ici on suppose qu'il arrive propre ou qu'on matche exact
            # Idéalement il faudrait normaliser avant
            user = User.objects.get(phone_number=phone_number)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

class PhonePINBackend(ModelBackend):
    """Authentification par numéro + code PIN"""
    def authenticate(self, request, phone_number=None, pin_code=None, **kwargs):
        if phone_number is None or pin_code is None:
            return None
        try:
            user = User.objects.get(phone_number=phone_number)
            if user.pin_code and user.check_pin(pin_code):
                return user
        except User.DoesNotExist:
            return None
