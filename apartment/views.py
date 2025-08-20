from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from apartment.forms import ContactForm
from reservations.models import Reservation


# Create your views here.
class IndexView(TemplateView):
    template_name = 'apartment/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            context['reservation'] = (
                Reservation.objects
                .filter(user=self.request.user)
                .order_by('-created_at')
                .first()
            )
        else:
            context['reservation'] = None

        return context


def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            send_mail(
                subject=f"[Сайт] {subject}",
                message=f"Име: {name}\nИмейл: {email}\n\nСъобщение:\n{message}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=["твояemail@example.com"],
            )

            messages.success(request, "Съобщението е изпратено успешно!")
            return redirect("index")
    else:
        form = ContactForm()

    return render(request, "apartment/contacts.html", {"form": form})