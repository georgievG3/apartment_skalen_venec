from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(label="Име", max_length=100)
    email = forms.EmailField(label="Имейл")
    subject = forms.CharField(max_length=100, label='Относно')
    message = forms.CharField(label="Съобщение", widget=forms.Textarea)