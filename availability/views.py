import requests
from django.shortcuts import render
from icalendar import Calendar
from rest_framework.views import APIView
from rest_framework.response import Response


BOOKING_ICAL_URL = "https://ical.booking.com/v1/export?t=016ddd1a-c963-4c2a-8678-ab408fe327ad"

class BookingAvailabilityView(APIView):
    def get(self, request):
        try:
            r = requests.get(BOOKING_ICAL_URL, timeout=10)
            r.raise_for_status()

            cal = Calendar.from_ical(r.text)
            events = []

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

            return Response(events)

        except Exception as e:
            return Response({"error": str(e)}, status=500)

