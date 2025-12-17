from django.urls import path
from . import views

app_name = 'member'

urlpatterns = [
    path('', views.MemberListView.as_view(), name='member_list'),
    path('<int:pk>/', views.MemberDetailView.as_view(), name='member_detail'),
    path('ajouter/', views.MemberCreateView.as_view(), name='member_add'),
    path('ajouter-plusieurs/', views.MemberBulkCreateView.as_view(), name='member_bulk_add'),
    path('<int:pk>/modifier/', views.MemberUpdateView.as_view(), name='member_edit'),
    path('<int:pk>/supprimer/', views.MemberDeleteView.as_view(), name='member_delete'),
    path('importer/', views.MemberImportView.as_view(), name='member_import'),
]
