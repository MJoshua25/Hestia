from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Member


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['first_name', 'last_name', 'phone_number', 'room_number', 'role']
        widgets = {
            'role': forms.Select(attrs={
                'class': 'input-ios w-full appearance-none bg-white pr-10'
            }),
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
            if field_name == 'first_name':
                field.widget.attrs['placeholder'] = 'Ex: Marie'
                field.widget.attrs['autocomplete'] = 'given-name'
            elif field_name == 'last_name':
                field.widget.attrs['placeholder'] = 'Ex: Dupont'
                field.widget.attrs['autocomplete'] = 'family-name'
            elif field_name == 'phone_number':
                field.widget.attrs['placeholder'] = 'Ex: 06 12 34 56 78'
                field.widget.attrs['autocomplete'] = 'tel'
                field.widget.attrs['inputmode'] = 'tel'
            elif field_name == 'room_number':
                field.widget.attrs['placeholder'] = 'Ex: 101'
                field.widget.attrs['inputmode'] = 'numeric'
