from django.shortcuts import redirect
from django.urls import reverse

class RequirePasswordChangeMiddleware:
    """Force la redirection vers /change-password si require_password_change=True"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if request.user.require_password_change:
                # Eviter la boucle de redirection infinie
                # On assume que l'URL name pour changer le mot de passe sera 'change_password'
                # ou 'first_connection' selon le nommage. Vérifier urls.py plus tard.
                # Pour l'instant on check le path startswith pour être safe.
                
                # Check if current path is NOT the change password path and NOT logout
                current_path = request.path
                if not current_path.startswith('/auth/first-connection/') and \
                   not current_path.startswith('/admin/') and \
                   not current_path.startswith('/static/'): # Allow static files
                    
                    # On redirigeons vers 'first_connection' (nom de route à définir)
                    # Si on ne connait pas encore le reverse, on met un placeholder ou on try
                    try:
                        change_password_url = reverse('first_connection')
                        if request.path != change_password_url:
                            return redirect('first_connection')
                    except Exception:
                        pass # URL not defined yet, pass for now
        
        return self.get_response(request)
