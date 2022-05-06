import datetime
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from model_mommy import mommy

from rentals.models import Rental, Reservation


class ReservationListViewTest(TestCase):

    def setUp(self) -> None:
        self.test_url = reverse('rentals:list')
        rental_1 = mommy.make(Rental, name='rental-1')
        mommy.make(
            Reservation,
            id=1,
            rental=rental_1,
            checkin=datetime.date(2022, 1, 1),
            checkout=datetime.date(2022, 1, 13),
        )
        mommy.make(
            Reservation,
            id=2,
            rental=rental_1,
            checkin=datetime.date(2022, 1, 20),
            checkout=datetime.date(2022, 2, 10),
        )
        mommy.make(
            Reservation,
            id=3,
            rental=rental_1,
            checkin=datetime.date(2022, 2, 20),
            checkout=datetime.date(2022, 3, 10),
        )
        rental_2 = mommy.make(Rental, name='rental-2')
        mommy.make(
            Reservation,
            id=4,
            rental=rental_2,
            checkin=datetime.date(2022, 1, 2),
            checkout=datetime.date(2022, 1, 20),
        )
        mommy.make(
            Reservation,
            id=5,
            rental=rental_2,
            checkin=datetime.date(2022, 1, 20),
            checkout=datetime.date(2022, 2, 11),
        )

    def test_get(self) -> None:
        response = self.client.get(self.test_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed('rentals/reservation_list.html')
        # The page should contain a table with a row for each reservation
        self.assertContains(
            response,
            '<tr><td>rental-1</td><td>Res-1</td><td>2022-01-01</td><td>2022-01-13</td><td>-</td></tr>',
            html=True,
        )
        # A row should reference a previous reservation if any
        self.assertContains(
            response,
            '<tr><td>rental-1</td><td>Res-2</td><td>2022-01-20</td><td>2022-02-10</td><td>Res-1</td></tr>',
            html=True,
        )
