from django.urls import path

from apartment.views import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
]