import requests
from icalendar import Calendar
from datetime import datetime
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from reservations.models import Reservation

BOOKING_ICAL_URL = "https://ical.booking.com/v1/export?t=016ddd1a-c963-4c2a-8678-ab408fe327ad"

class BookingAvailabilityView(APIView):
    def get(self, request):
        events = []

        try:
            r = requests.get(BOOKING_ICAL_URL, timeout=10)
            r.raise_for_status()
            cal = Calendar.from_ical(r.text)
            for component in cal.walk():
                if component.name == "VEVENT":
                    start = component.get('dtstart').dt
                    end = component.get('dtend').dt
                    events.append({
                        "title": "Заето",
                        "start": start.strftime("%Y-%m-%d"),
                        "end": end.strftime("%Y-%m-%d"),
                        "color": "red"
                    })
        except Exception as e:
            print("Booking iCal error:", e)

        paid_reservations = Reservation.objects.filter(status='paid')
        for r in paid_reservations:
            events.append({
                "title": "Заето",
                "start": r.start_date.strftime("%Y-%m-%d"),
                "end": r.end_date.strftime("%Y-%m-%d"),
                "color": "red"
            })

        return Response(events)


def reservation_page(request):
    return render(request, 'reservations/reservation.html')
