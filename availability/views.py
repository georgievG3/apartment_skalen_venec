import requests
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from reservations.models import Reservation
from icalendar import Calendar, Event
from datetime import datetime, timedelta
import pytz

BOOKING_ICAL_URL = "https://ical.booking.com/v1/export?t=d10c9360-24c7-4970-85ff-7ada13f9794b"

class BookingAvailabilityView(APIView):
    def get(self, request):
        events = []

        try:
            r = requests.get(BOOKING_ICAL_URL, timeout=10)
            r.raise_for_status()
            cal = Calendar.from_ical(r.content)  # content вместо text

            for component in cal.walk():
                if component.name == "VEVENT":
                    start = component.get('dtstart').dt
                    end = component.get('dtend').dt

                    if isinstance(start, datetime):
                        start = start.date()
                    if isinstance(end, datetime):
                        end = end.date()

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

def reservations_ical(request):
    cal = Calendar()
    cal.add('prodid', '-//My Apartment Booking//example.com//')
    cal.add('version', '2.0')

    reservations = Reservation.objects.filter(status='paid')
    tz = pytz.timezone('Europe/Sofia')

    for r in reservations:
        event = Event()
        event.add('summary', 'Заето')
        # iCal използва края на деня като dtend, затова добавяме 1 ден
        event.add('dtstart', tz.localize(datetime.combine(r.start_date, datetime.min.time())))
        event.add('dtend', tz.localize(datetime.combine(r.end_date, datetime.min.time())))
        event.add('description', f'Резервация от {r.name} {r.surname}')
        cal.add_component(event)

    response = HttpResponse(cal.to_ical(), content_type='text/calendar')
    response['Content-Disposition'] = 'inline; filename="reservations.ics"'
    return response


def reservation_page(request):
    return render(request, 'reservations/reservation.html')
