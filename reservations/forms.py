from django import forms
from .models import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['name', 'surname', 'email', 'phone', 'people',  'start_date', 'end_date', 'notes']
        widgets = {
            'start_date': forms.TextInput(attrs={'readonly': 'readonly'}),
            'end_date': forms.TextInput(attrs={'readonly': 'readonly'}),
            'notes': forms.Textarea(attrs={"style": "resize: none; outline: none;"}),
        }

        labels = {
            'name': 'Име',
            'surname': 'Фамилия',
            'email': 'Имейл',
            'phone': 'Телефон',
            'people': 'Брой гости',
            'start_date': 'От',
            'end_date': 'До',
            'notes': 'Допълнителна информация'
        }