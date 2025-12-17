from django import forms
from .models import Event, Commission
from django.utils.translation import gettext_lazy as _


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'location']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Apple HIG-inspired input styling with 44px touch target
        input_class = 'input-ios w-full'
        
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = input_class
            
            # Add focus ring styling
            field.widget.attrs['class'] += ' focus:outline-none'
            
            # Add placeholder for better UX
            if field_name == 'title':
                field.widget.attrs['placeholder'] = 'Ex: Soirée de Noël'
            elif field_name == 'location':
                field.widget.attrs['placeholder'] = 'Ex: Salle principale'
            elif field_name == 'description':
                field.widget.attrs['placeholder'] = 'Décrivez les détails de l\'événement...'


class CommissionForm(forms.ModelForm):
    class Meta:
        model = Commission
        fields = ['name', 'description', 'max_capacity']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Apple HIG-inspired input styling with 44px touch target
        input_class = 'input-ios w-full'
        
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = input_class
            
            # Add focus ring styling
            field.widget.attrs['class'] += ' focus:outline-none'
            
            # Add placeholder for better UX
            if field_name == 'name':
                field.widget.attrs['placeholder'] = 'Ex: Décoration, Cuisine, Animation...'
            elif field_name == 'description':
                field.widget.attrs['placeholder'] = 'Décrivez les responsabilités de cette commission...'
            elif field_name == 'max_capacity':
                field.widget.attrs['inputmode'] = 'numeric'
