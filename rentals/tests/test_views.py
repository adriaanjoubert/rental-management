import datetime
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from model_mommy import mommy

from rentals.models import Rental, Reservation


class ReservationListViewTest(TestCase):

    def setUp(self) -> None:
        self.test_url = reverse('rentals:reservation_list')
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


class ReservationCreateViewTest(TestCase):

    def setUp(self) -> None:
        self.rental = mommy.make(Rental, name='rental-1')
        self.test_url = reverse('rentals:reservation_create')

    def test_get(self) -> None:
        response = self.client.get(self.test_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed('rentals/rental_form.html')

    def test_valid_post(self) -> None:
        post_data = {
            'rental': self.rental.id,
            'checkin': '2022-01-01',
            'checkout': '2022-01-02',
        }
        response = self.client.post(self.test_url, data=post_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.test_url)
        self.assertEqual(Reservation.objects.count(), 1)
        reservation = Reservation.objects.first()
        self.assertEqual(reservation.rental, self.rental)
        self.assertEqual(reservation.checkin, datetime.date(2022, 1, 1))
        self.assertEqual(reservation.checkout, datetime.date(2022, 1, 2))

    def test_invalid_post(self) -> None:
        post_data = {
            'rental': self.rental.id,
            'checkin': 'a',
            'checkout': '2022-01-02',
        }
        response = self.client.post(self.test_url, data=post_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Enter a valid date.')
        self.assertEqual(Reservation.objects.count(), 0)


class RentalCreateViewTest(TestCase):

    def setUp(self) -> None:
        self.test_url = reverse('rentals:rental_create')

    def test_get(self) -> None:
        response = self.client.get(self.test_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed('rentals/rental_list.html')
