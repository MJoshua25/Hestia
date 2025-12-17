from django.urls import path
from .views import (
    EventListView, EventDetailView, EventCreateView, EventUpdateView, EventDeleteView,
    CommissionCreateView, CommissionUpdateView, CommissionDeleteView
)

urlpatterns = [
    path('', EventListView.as_view(), name='event_list'),
    path('create/', EventCreateView.as_view(), name='event_create'),
    path('<int:pk>/', EventDetailView.as_view(), name='event_detail'),
    path('<int:pk>/update/', EventUpdateView.as_view(), name='event_update'),
    path('<int:pk>/delete/', EventDeleteView.as_view(), name='event_delete'),
    
    # Commissions
    path('<int:event_id>/commission/create/', CommissionCreateView.as_view(), name='commission_create'),
    path('commission/<int:pk>/update/', CommissionUpdateView.as_view(), name='commission_update'),
    path('commission/<int:pk>/delete/', CommissionDeleteView.as_view(), name='commission_delete'),
]
