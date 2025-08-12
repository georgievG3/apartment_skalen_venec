from django.contrib.auth.views import LogoutView
from django.urls import path

from accounts.views import RegisterView, Login

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', Login.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]