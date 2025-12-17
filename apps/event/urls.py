from django.urls import path
from .views import (
    EventListView, EventDetailView, EventCreateView, EventUpdateView, EventDeleteView,
    CommissionCreateView, CommissionUpdateView, CommissionDeleteView, CommissionDetailView,
    CommissionManageView, CommissionDataAPI, AssignmentAutoAPI, AssignmentManualAPI,
    export_commissions_excel, export_commissions_pdf
)

urlpatterns = [
    path('', EventListView.as_view(), name='event_list'),
    path('creer/', EventCreateView.as_view(), name='event_create'),
    path('<int:pk>/', EventDetailView.as_view(), name='event_detail'),
    path('<int:pk>/modifier/', EventUpdateView.as_view(), name='event_update'),
    path('<int:pk>/supprimer/', EventDeleteView.as_view(), name='event_delete'),
    
    # Commissions
    path('<int:event_id>/commission/creer/', CommissionCreateView.as_view(), name='commission_create'),
    path('commission/<int:pk>/', CommissionDetailView.as_view(), name='commission_detail'),
    path('commission/<int:pk>/modifier/', CommissionUpdateView.as_view(), name='commission_update'),
    path('commission/<int:pk>/supprimer/', CommissionDeleteView.as_view(), name='commission_delete'),
    
    # Commission Management & API
    path('<int:event_id>/commissions/gerer/', CommissionManageView.as_view(), name='commission_manage'),
    path('<int:event_id>/api/commissions/', CommissionDataAPI.as_view(), name='commission_data_api'),
    path('<int:event_id>/api/assign/auto/', AssignmentAutoAPI.as_view(), name='assign_auto_api'),
    path('<int:event_id>/api/assign/manual/', AssignmentManualAPI.as_view(), name='assign_manual_api'),
    path('<int:event_id>/export/excel/', export_commissions_excel, name='export_commissions_excel'),
    path('<int:event_id>/export/pdf/', export_commissions_pdf, name='export_commissions_pdf'),
]
