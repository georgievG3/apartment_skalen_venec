from django.shortcuts import render
from django.views.generic import ListView, TemplateView


# Create your views here.
class IndexView(TemplateView):
    template_name = 'apartment/index.html'

