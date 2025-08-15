from django.urls import path
from .views import BookingAvailabilityView

urlpatterns = [
    path("booking/", BookingAvailabilityView.as_view(), name="booking-availability"),
]