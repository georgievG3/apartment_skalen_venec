from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from reservations.forms import ReservationForm
from reservations.models import Reservation
from availability.views import BookingAvailabilityView
from rest_framework.test import APIRequestFactory
from datetime import datetime
from django.template.loader import render_to_string
from django.core.mail import send_mail

import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


def create_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data['start_date']
            end = form.cleaned_data['end_date']

            conflicts = Reservation.objects.filter(
                start_date__lt=end,
                end_date__gt=start,
                status='paid'
            )
            if conflicts.exists():
                form.add_error(None, "Избраните дати вече са заети.")
                return render(request, 'reservations/reservation.html', {'form': form})

            nights = (end - start).days
            if nights <= 0:
                form.add_error(None, "Крайната дата трябва да е след началната.")
                return render(request, 'reservations/reservation.html', {'form': form})

            total_amount = nights * settings.PRICE_PER_NIGHT
            amount_in_minor = int(total_amount * 100)

            success_url = request.build_absolute_uri(reverse('payment_success')) + "?session_id={CHECKOUT_SESSION_ID}"
            cancel_url = request.build_absolute_uri(reverse('payment_cancel'))

            checkout_session = stripe.checkout.Session.create(
                mode="payment",
                payment_method_types=["card"],
                line_items=[{
                    "price_data": {
                        "currency": settings.CURRENCY,
                        "product_data": {
                            "name": f"Резервация {start} → {end}",
                            "description": f"{nights} нощувки x {settings.PRICE_PER_NIGHT} {settings.CURRENCY.upper()}",
                        },
                        "unit_amount": amount_in_minor,
                    },
                    "quantity": 1,
                }],
                metadata={
                    "start_date": str(start),
                    "end_date": str(end),
                    "nights": str(nights),
                    "name": form.cleaned_data['name'],
                    "surname": form.cleaned_data['surname'],
                    "email": form.cleaned_data['email'],
                    "phone": form.cleaned_data['phone'],
                    "people": str(form.cleaned_data['people']),
                    "notes": form.cleaned_data.get('notes', ''),
                    "user_id": str(request.user.id) if request.user.is_authenticated else ''
                },
                success_url=success_url,
                cancel_url=cancel_url,
            )

            return redirect(checkout_session.url, code=303)
    else:
        form = ReservationForm()

    return render(request, 'reservations/reservation.html', {'form': form})



@csrf_exempt
def stripe_webhook(request):
    import traceback
    from django.core.mail import send_mail
    from django.template.loader import render_to_string
    from django.contrib.auth import get_user_model
    User = get_user_model()

    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")

    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=sig_header,
            secret=settings.STRIPE_WEBHOOK_SECRET
        )
    except Exception:
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        metadata = session.get("metadata", {})

        try:
            start_date = datetime.strptime(metadata.get('start_date'), "%Y-%m-%d").date()
            end_date = datetime.strptime(metadata.get('end_date'), "%Y-%m-%d").date()
            nights = (end_date - start_date).days
            total_price = nights * settings.PRICE_PER_NIGHT
            user = None
            user_id = metadata.get('user_id')
            if user_id:
                try:
                    user = User.objects.get(id=int(user_id))
                except User.DoesNotExist:
                    user = None

            reservation = Reservation.objects.create(
                name=metadata.get('name', ''),
                surname=metadata.get('surname', ''),
                email=metadata.get('email', ''),
                phone=metadata.get('phone', ''),
                people=int(metadata.get('people', '1')),
                start_date=start_date,
                end_date=end_date,
                notes=metadata.get('notes', ''),
                status='paid',
                user=user
            )

            if reservation.email:
                message_client = render_to_string(
                    'reservations/email-confirmation.html',
                    {'reservation': reservation}
                )
                send_mail(
                    f"Потвърждение за резервация #{reservation.id}",
                    message_client,
                    settings.DEFAULT_FROM_EMAIL,
                    [reservation.email],
                    fail_silently=True
                )

            message_owner = (
                f"Имате нова резервация:\n\n"
                f"Клиент: {reservation.name} {reservation.surname}\n"
                f"Имейл: {reservation.email}\n"
                f"Телефон: {reservation.phone}\n"
                f"Период: {reservation.start_date} → {reservation.end_date}\n"
                f"Общо нощувки: {nights}\n"
                f"Брой хора: {reservation.people}\n"
                f"Бележки: {reservation.notes or 'няма'}\n\n"
                f"Обща цена: {total_price} {settings.CURRENCY.upper()}"
            )
            send_mail(
                f"Нова платена резервация #{reservation.id}",
                message_owner,
                settings.DEFAULT_FROM_EMAIL,
                [settings.DEFAULT_FROM_EMAIL],
                fail_silently=True
            )

        except Exception:
            traceback.print_exc()

    return HttpResponse(status=200)



def payment_success(request):
    messages.success(request, "Успешно резервирахте апартамента!")
    return redirect('index')


def payment_cancel(request):
    return render(request, 'reservations/cancel.html')
