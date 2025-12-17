from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

User = get_user_model()

class LoginView(View):
    template_name = 'auth/login.html'

    def get(self, request):
        """Gère l'affichage du formulaire de connexion."""
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, self.template_name)

    def post(self, request):
        """Gère l'authentification avec 3 méthodes."""
        if request.user.is_authenticated:
            return redirect('home')
            
        method = request.POST.get('method')
        user = None
        print(f"Method: {method}")
        print(f"POST data: {request.POST}")
        
        if method == "username_password":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            
        elif method == "phone_password":
            phone = request.POST.get('phone')
            password = request.POST.get('password')
            user = authenticate(request, phone_number=phone, password=password)
            
        elif method == "phone_pin":
            phone = request.POST.get('phone')
            pin = request.POST.get('pin')
            
            print(f"Phone: {phone}, PIN: {pin}")
            # Assuming the backend expects 'pin_code' not 'pin', but authenticate uses kwargs matching backend signautre
            # Check backend signature: authenticate(self, request, phone_number=None, pin_code=None, **kwargs)
            user = authenticate(request, phone_number=phone, pin_code=pin)
            
        if user is not None:
            login(request, user)
            # Gestion "Se souvenir de moi"
            if request.POST.get('remember_me'):
                request.session.set_expiry(7776000) # 90 jours
            else:
                request.session.set_expiry(2592000) # 30 jours (default)
                
            return redirect('home')
        else:
            messages.error(request, "Identifiants incorrects.")
            return render(request, self.template_name)

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

@method_decorator(login_required, name='dispatch')
class FirstConnectionView(View):
    """Vue pour changement de mot de passe obligatoire et définition PIN"""
    template_name = 'auth/first_connection.html'

    def get(self, request):
        # Si l'utilisateur n'a pas besoin de changer son mdp, on redirige
        if not request.user.require_password_change:
            return redirect('home')
        return render(request, self.template_name)

    def post(self, request):
        # Si l'utilisateur n'a pas besoin de changer son mdp, on redirige
        if not request.user.require_password_change:
            return redirect('home')

        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        pin_code = request.POST.get('pin_code')
        
        if new_password != confirm_password:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return render(request, self.template_name)
            
        if len(new_password) < 8:
             messages.error(request, "Le mot de passe doit contenir au moins 8 caractères.")
             return render(request, self.template_name)

        # Update password
        request.user.set_password(new_password)
        request.user.require_password_change = False
        
        # Update PIN if provided
        if pin_code and len(pin_code) == 6 and pin_code.isdigit():
             request.user.set_pin(pin_code)
        
        request.user.save()
        
        # Re-login user because changing password logs them out
        # Specify backend to avoid ambiguity with multiple backends
        login(request, request.user, backend='django.contrib.auth.backends.ModelBackend')
        
        messages.success(request, "Compte configuré avec succès !")
        return redirect('home')

@method_decorator(login_required, name='dispatch')
class ResetPasswordView(View):
    """Permet à un Admin/Déléguée de réinitialiser le mdp d'un membre"""

    def dispatch(self, request, *args, **kwargs):
        # Vérification des droits (Admin ou Déléguée)
        if not request.user.is_superuser:
            try:
                requester_profile = request.user.member_profile
                if not (requester_profile.is_admin or requester_profile.is_delegate):
                    messages.error(request, "Vous n'avez pas les droits pour effectuer cette action.")
                    return redirect('home')
            except AttributeError:
                 messages.error(request, "Vous n'avez pas les droits pour effectuer cette action.")
                 return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, user_id):
        try:
            target_user = User.objects.get(id=user_id)
            # Reset password to default
            target_user.set_password("pass_Default1")
            target_user.require_password_change = True
            target_user.save()
            messages.success(request, f"Mot de passe de {target_user.username} réinitialisé avec succès.")
        except User.DoesNotExist:
            messages.error(request, "Utilisateur introuvable.")
        
        # Rediriger vers la page précédente ou la liste des membres
        return redirect(request.META.get('HTTP_REFERER', 'home'))

@method_decorator(login_required, name='dispatch')
class DeletePinView(View):
    """Permet à un Admin/Déléguée de supprimer le PIN d'un membre"""
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            try:
                requester_profile = request.user.member_profile
                if not (requester_profile.is_admin or requester_profile.is_delegate):
                    messages.error(request, "Vous n'avez pas les droits pour effectuer cette action.")
                    return redirect('home')
            except AttributeError:
                 messages.error(request, "Vous n'avez pas les droits pour effectuer cette action.")
                 return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, user_id):
        try:
            target_user = User.objects.get(id=user_id)
            target_user.pin_code = None
            target_user.save()
            messages.success(request, f"Code PIN de {target_user.username} supprimé avec succès.")
        except User.DoesNotExist:
            messages.error(request, "Utilisateur introuvable.")
            
        return redirect(request.META.get('HTTP_REFERER', 'home'))
        return redirect(request.META.get('HTTP_REFERER', 'home'))

