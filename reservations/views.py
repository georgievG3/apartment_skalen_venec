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
                status__in=['pending', 'paid']
            )
            if conflicts.exists():
                form.add_error(None, "Избраните дати вече са заети.")
                return render(request, 'reservations/reservation.html', {'form': form})

            factory = APIRequestFactory()
            api_request = factory.get('/api/availability/booking/')
            view = BookingAvailabilityView.as_view()
            response = view(api_request)
            events = response.data

            for e in events:
                booked_start = datetime.strptime(e['start'], "%Y-%m-%d").date()
                booked_end = datetime.strptime(e['end'], "%Y-%m-%d").date()
                if start < booked_end and end > booked_start:
                    form.add_error(None, "Избраните дати вече са заети (Booking).")
                    return render(request, 'reservations/reservation.html', {'form': form})

            nights = (end - start).days
            if nights <= 0:
                form.add_error(None, "Крайната дата трябва да е след началната.")
                return render(request, 'reservations/reservation.html', {'form': form})

            reservation = form.save(commit=False)
            reservation.status = 'pending'
            reservation.user = request.user
            reservation.save()

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
                            "name": f"Резервация {reservation.start_date} → {reservation.end_date}",
                            "description": f"{nights} нощувки x {settings.PRICE_PER_NIGHT} {settings.CURRENCY.upper()}",
                        },
                        "unit_amount": amount_in_minor,
                    },
                    "quantity": 1,
                }],
                metadata={
                    "reservation_id": str(reservation.id),
                    "start_date": str(reservation.start_date),
                    "end_date": str(reservation.end_date),
                    "nights": str(nights),
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
        reservation_id = session.get("metadata", {}).get("reservation_id")
        if reservation_id:
            try:
                reservation = Reservation.objects.get(id=reservation_id)
                reservation.status = 'paid'
                reservation.save()

                if getattr(reservation, "email", None):
                    subject = f"Потвърждение за резервация #{reservation.id}"
                    message = render_to_string('reservations/email-confirmation.html', {
                        'reservation': reservation
                    })
                    send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        [reservation.email],
                        fail_silently=True,
                    )
            except Exception:
                print("Stripe webhook error:")
                traceback.print_exc()

    return HttpResponse(status=200)

def payment_success(request):
    messages.success(request, "Успешно резервирахте апартамента!")
    return redirect('index')

def payment_cancel(request):
    return render(request, 'reservations/cancel.html')