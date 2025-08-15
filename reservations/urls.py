from django.urls import path

from reservations.views import  create_reservation

urlpatterns = [
    path('new', create_reservation, name="create_reservation"),
]