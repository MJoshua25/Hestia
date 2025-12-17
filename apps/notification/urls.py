from django.urls import path
from . import views

app_name = 'notification'

urlpatterns = [
    path('', views.NotificationListView.as_view(), name='list'),
    path('api/unread/', views.get_unread_notifications, name='get_unread'),
    path('api/mark-read/<int:pk>/', views.mark_as_read, name='mark_as_read'),
    path('api/mark-all-read/', views.mark_all_as_read, name='mark_all_as_read'),
    path('api/delete/<int:pk>/', views.delete_notification, name='delete'),
    path('api/toggle-read/<int:pk>/', views.toggle_read_status, name='toggle_read'),
]
