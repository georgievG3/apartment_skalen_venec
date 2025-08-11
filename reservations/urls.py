from django.urls import path

from reservations.views import ReservationView

urlpatterns = [
    path('reserve', ReservationView.as_view(), name="reservation"),
]