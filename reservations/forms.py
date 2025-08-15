from django import forms
from .models import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['name', 'surname', 'email', 'phone', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.TextInput(attrs={'readonly': 'readonly'}),
            'end_date': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

        labels = {
            'name': 'Име',
            'surname': 'Фамилия',
            'email': 'Имейл',
            'phone': 'Телефон',
            'start_date': 'От',
            'end_date': 'До'
        }