from django import forms
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox


class ContactForm(forms.Form):
    name = forms.CharField(label="Име", max_length=100)
    email = forms.EmailField(label="Имейл")
    subject = forms.CharField(max_length=100, label='Относно')
    message = forms.CharField(label="Съобщение", widget=forms.Textarea)

    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox
    )