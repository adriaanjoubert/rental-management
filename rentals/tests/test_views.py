import datetime
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from model_mommy import mommy

from rentals.models import Rental, Reservation


class ReservationListViewTest(TestCase):

    def setUp(self) -> None:
        self.test_url = reverse('rentals:list')
        rental = mommy.make(Rental, name='rental-1')
        mommy.make(Reservation, rental=rental, checkin=datetime.date(2022, 1, 1), checkout=datetime.date(2022, 1, 13))

    def test_get(self) -> None:
        response = self.client.get(self.test_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed('rentals/list.html')
        # The page should contain a table with a row for each reservation
        self.assertContains(
            response,
            '<td>rental-1</td><td>Res-1 ID</td><td>2022-01-01</td><td>2022-01-13</td><td>-</td>',
            html=True,
        )
        # A row should reference a previous reservation if any
        self.assertContains(
            response,
            '<td>rental-1</td><td>Res-2 ID</td><td>2022-01-20</td><td>2022-02-10</td><td>Res-1 ID</td>',
            html=True,
        )
