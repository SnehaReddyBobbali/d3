from django import forms
from .models import LostItem, Claim


class LostItemForm(forms.ModelForm):
    """Form for creating and updating lost items"""
    
    class Meta:
        model = LostItem
        fields = ['title', 'description', 'category', 'status', 'location_lost', 
                  'date_lost', 'image', 'contact_info']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Black Laptop Bag'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Provide detailed description...',
                'rows': 4
            }),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'location_lost': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Library 2nd Floor'
            }),
            'date_lost': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'contact_info': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone or Email'
            }),
        }


class ClaimForm(forms.ModelForm):
    """Form for claiming lost items"""
    
    class Meta:
        model = Claim
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe why this item belongs to you...',
                'rows': 4
            }),
        }
