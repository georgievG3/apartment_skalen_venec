from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from accounts.forms import AppUserCreationForm, AuthForm
from reservations.models import Reservation

# Create your views here.

UserModel = get_user_model()

class RegisterView(CreateView):
    model = UserModel
    form_class = AppUserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        response = super().form_valid(form)

        if response.status_code in [301, 302]:
            login(self.request, self.object)

        return response


class Login(LoginView):
    authentication_form = AuthForm


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/user-profile.html"


