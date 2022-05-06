from django.views.generic import ListView

from rentals.models import Reservation


class ReservationListView(ListView):
    model = Reservation
    paginate_by = 50
