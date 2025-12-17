from django.urls import path
from .views import HomeView, LoginView, LogoutView, FirstConnectionView, ResetPasswordView, DeletePinView


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/first-connection/', FirstConnectionView.as_view(), name='first_connection'),
    path('auth/reset-password/<int:user_id>/', ResetPasswordView.as_view(), name='reset_password'),
    path('auth/delete-pin/<int:user_id>/', DeletePinView.as_view(), name='delete_pin'),
]
