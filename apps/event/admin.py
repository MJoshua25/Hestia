from django.contrib import admin
from .models import Event, Commission

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'statut')
    list_filter = ('date', 'statut')
    search_fields = ('title', 'location')

@admin.register(Commission)
class CommissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'event', 'max_capacity', 'statut')
    list_filter = ('event', 'statut')
    search_fields = ('name', 'event__title')
