from django.contrib import admin
from .models import Member

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'role', 'phone_number', 'room_number', 'statut')
    list_filter = ('role', 'statut')
    search_fields = ('first_name', 'last_name', 'phone_number')
