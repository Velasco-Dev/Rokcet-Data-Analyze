from django import forms
from .models import DataFile

class DataFileForm(forms.ModelForm):
    class Meta:
        model = DataFile
        fields = ['name', 'file', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del análisis',
                'required': True
            }),
            'file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.csv',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción (opcional)',
                'rows': 3
            })
        }