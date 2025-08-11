from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.
class ReservationView(TemplateView):
    template_name = 'reservations/reservation.html'