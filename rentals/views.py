from django.db import models
from django.db.models import OuterRef, QuerySet, Subquery
from django.views.generic import ListView

from rentals.models import Reservation


class ReservationListView(ListView):
    model = Reservation
    paginate_by = 50
    context_object_name = 'reservations'

    def get_queryset(self) -> 'QuerySet[Reservation]':
        previous_reservations = Reservation.objects.filter(
            rental_id=OuterRef('rental_id'),
            checkin__lt=OuterRef('checkin'),
        ).order_by('-checkin')
        return Reservation.objects.all().annotate(
            previous_reservation_id=Subquery(previous_reservations.values('id')[:1], output_field=models.CharField())
        ).select_related('rental')
