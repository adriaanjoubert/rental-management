from django.db import models
from django.utils import timezone


class Rental(models.Model):
    name = models.CharField(max_length=128)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f'{self.name}'


class Reservation(models.Model):
    rental = models.ForeignKey(Rental, on_delete=models.PROTECT)
    checkin = models.DateField()
    checkout = models.DateField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['rental', 'checkin']
