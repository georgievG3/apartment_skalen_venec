from django.urls import path, include

from apartment.views import IndexView, contact_view, RulesView, AboutUsView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('contacts/', contact_view, name='contacts'),
    path('rules/', RulesView.as_view(), name='rules'),
    path('about-us/', AboutUsView.as_view(), name='about-us'),
    path('captcha/', include('captcha.urls')),
]