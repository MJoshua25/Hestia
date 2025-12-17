from django import forms
from .models import Event, Commission
from django.utils.translation import gettext_lazy as _


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'location']
        widgets = {
            'date': forms.DateTimeInput(attrs={'class': 'flatpickr-datetime'}),
            'description': forms.Textarea(attrs={'class': 'quill-editor', 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Apple HIG-inspired input styling with 44px touch target
        input_class = 'input-ios w-full'
        
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = input_class
            else:
                field.widget.attrs['class'] += f' {input_class}'
            
            # Add focus ring styling
            field.widget.attrs['class'] += ' focus:outline-none'
            
            # Add placeholder for better UX
            if field_name == 'title':
                field.widget.attrs['placeholder'] = 'Ex: Soirée de Noël'
            elif field_name == 'location':
                field.widget.attrs['placeholder'] = 'Ex: Salle principale'
            # Description placeholder handled by Quill or attrs if Quill fails
            
class CommissionForm(forms.ModelForm):
    class Meta:
        model = Commission
        fields = ['name', 'description', 'min_capacity', 'max_capacity', 'responsible']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'quill-editor', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Apple HIG-inspired input styling with 44px touch target
        input_class = 'input-ios w-full'
        
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = input_class
            else:
                field.widget.attrs['class'] += f' {input_class}'
            
            # Add focus ring styling

            field.widget.attrs['class'] += ' focus:outline-none'
            
            # Add placeholder for better UX
            if field_name == 'name':
                field.widget.attrs['placeholder'] = 'Ex: Décoration, Cuisine, Animation...'
            elif field_name == 'description':
                field.widget.attrs['placeholder'] = 'Décrivez les responsabilités de cette commission...'
            elif field_name == 'max_capacity':
                field.widget.attrs['inputmode'] = 'numeric'
