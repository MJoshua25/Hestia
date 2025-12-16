from django.urls import path
from . import views

app_name = 'member'

urlpatterns = [
    path('', views.MemberListView.as_view(), name='member_list'),
    path('<int:pk>/', views.MemberDetailView.as_view(), name='member_detail'),
    path('add/', views.MemberCreateView.as_view(), name='member_add'),
    path('<int:pk>/edit/', views.MemberUpdateView.as_view(), name='member_edit'),
    path('<int:pk>/delete/', views.MemberDeleteView.as_view(), name='member_delete'),
    path('import/', views.MemberImportView.as_view(), name='member_import'),
]
