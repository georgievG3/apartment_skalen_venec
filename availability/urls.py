from django.urls import path
from .views import BookingAvailabilityView, reservations_ical

urlpatterns = [
    path("booking/", BookingAvailabilityView.as_view(), name="booking-availability"),
    path('ical/reservations.ics', reservations_ical, name='reservations_ical'),
]