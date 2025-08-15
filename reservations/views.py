from django.shortcuts import render
from reservations.forms import ReservationForm
from reservations.models import Reservation
from availability.views import BookingAvailabilityView
from rest_framework.test import APIRequestFactory
from datetime import datetime


# Create your views here.

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

            reservation = form.save(commit=False)
            reservation.status = 'pending'
            reservation.save()
            return render(request, 'reservations/success.html', {'reservation': reservation})
    else:
        form = ReservationForm()
    return render(request, 'reservations/reservation.html', {'form': form})