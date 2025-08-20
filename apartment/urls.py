from django.urls import path

from apartment.views import IndexView, contact_view

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('contacts/', contact_view, name='contacts'),
]