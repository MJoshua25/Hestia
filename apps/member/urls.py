from django.urls import path
from . import views

app_name = 'member'

urlpatterns = [
    path('', views.MemberListView.as_view(), name='member_list'),
    path('profil/', views.ProfileView.as_view(), name='profile'),
    path('profil/password/', views.change_password, name='change_password'),
    path('profil/pin/', views.manage_pin, name='manage_pin'),
    path('profil/photo/delete/', views.delete_photo, name='delete_photo'),
    path('<int:pk>/', views.MemberDetailView.as_view(), name='member_detail'),
    path('ajouter/', views.MemberCreateView.as_view(), name='member_add'),
    path('ajouter-plusieurs/', views.MemberBulkCreateView.as_view(), name='member_bulk_add'),
    path('<int:pk>/modifier/', views.MemberUpdateView.as_view(), name='member_edit'),
    path('<int:pk>/supprimer/', views.MemberDeleteView.as_view(), name='member_delete'),
    path('<int:pk>/archiver/', views.archive_member, name='member_archive'),
    path('<int:pk>/restaurer/', views.restore_member, name='member_restore'),
    path('<int:pk>/supprimer-def/', views.delete_member_permanently, name='member_delete_permanent'),
    path('importer/', views.MemberImportView.as_view(), name='member_import'),
]
