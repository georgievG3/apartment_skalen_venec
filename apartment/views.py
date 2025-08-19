from django.views.generic import TemplateView

from reservations.models import Reservation


# Create your views here.
class IndexView(TemplateView):
    template_name = 'apartment/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['reservation'] = Reservation.objects.filter(user=self.request.user).order_by('-created_at').first()
        return context