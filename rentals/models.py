from django.db import models


class Rental(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self) -> str:
        return f'{self.name}'


class Reservation(models.Model):
    rental = models.ForeignKey(Rental, on_delete=models.PROTECT)
    checkin = models.DateField()
    checkout = models.DateField()

    class Meta:
        ordering = ['rental', 'checkin']
