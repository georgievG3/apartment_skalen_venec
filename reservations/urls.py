from django.urls import path

from reservations.views import create_reservation, payment_success, payment_cancel, stripe_webhook

urlpatterns = [
    path('new', create_reservation, name="create_reservation"),
    path('payment/success/', payment_success, name='payment_success'),
    path('payment/cancel/', payment_cancel, name='payment_cancel'),
    path('stripe/webhook/', stripe_webhook, name='stripe-webhook'),
]
