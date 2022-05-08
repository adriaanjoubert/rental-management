from typing import Any, Dict

from django.db import models
from django.db.models import OuterRef, QuerySet, Subquery
from django.urls import reverse
from django.views.generic import CreateView, ListView

from rentals.models import Rental, Reservation


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


class RentalCreateView(CreateView):
    model = Rental
    fields = ['name']

    def get_success_url(self) -> str:
        return reverse('rentals:rental_create')

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['rentals'] = Rental.objects.all()
        return context


class ReservationCreateView(CreateView):
    model = Reservation
    fields = ['rental', 'checkin', 'checkout']

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['rentals_count'] = Rental.objects.count()
        return context

    def get_success_url(self) -> str:
        return reverse('rentals:reservation_create')
