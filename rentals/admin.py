from django.contrib import admin
from django.contrib.admin import register

from rentals.models import Rental, Reservation


@register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    autocomplete_fields = ['rental']
    list_display = ['rental', 'checkin', 'checkout']
    list_filter = ['checkin', 'checkout']
