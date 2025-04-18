from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from .models import Table, Reservation

from .helpers import get_seat_cost


class BookingCancelAPITestCase(APITestCase):
    def setUp(self):
        self.seat_cost = get_seat_cost()
        self.user = User.objects.create_user(email="rr@g.com", password="pass123")
        self.client.force_login(self.user)

        Table.objects.bulk_create(
            [
                Table(seats=4, is_available=True),
                Table(seats=6, is_available=True),
                Table(seats=8, is_available=True),
            ]
        )

        self.reserve_url = reverse("reservations")

    def test_even_number_booking(self):
        response = self.client.post(
            self.reserve_url, {"number_of_people": 2}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        res = Reservation.objects.get(user=self.user)
        self.assertEqual(res.seats, 2)
        self.assertEqual(res.cost, 2 * self.seat_cost)

    def test_odd_number_round_up(self):
        response = self.client.post(
            self.reserve_url, {"number_of_people": 1}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        res = Reservation.objects.get(user=self.user)
        self.assertEqual(res.seats, 2)
        self.assertEqual(res.cost, 2 * self.seat_cost)

    def test_full_table_when_equal(self):
        response = self.client.post(
            self.reserve_url, {"number_of_people": 6}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        res = Reservation.objects.get(user=self.user)
        self.assertEqual(res.seats, 6)
        self.assertEqual(res.cost, (6 - 1) * self.seat_cost)

    def test_no_available_tables(self):
        Table.objects.update(is_available=False)
        resp = self.client.post(
            self.reserve_url, {"number_of_people": 2}, format="json"
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_reservations(self):
        for num in (2, 4):
            self.client.post(self.reserve_url, {"number_of_people": num}, format="json")
        resp = self.client.get(self.reserve_url, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        self.assertEqual(len(data), 2)
        for item in data:
            self.assertIn("id", item)
            self.assertIn("table", item)
            self.assertIn("seats", item)
            self.assertIn("cost", item)

    def test_retrieve_reservation(self):
        book_resp = self.client.post(
            self.reserve_url, {"number_of_people": 2}, format="json"
        )
        res_id = book_resp.json()["id"]
        detail_url = reverse("reservation", args=[res_id])
        resp = self.client.get(detail_url, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.json()["id"], res_id)

    def test_cancel_reservation(self):
        book_resp = self.client.post(
            self.reserve_url, {"number_of_people": 2}, format="json"
        )
        res_id = book_resp.json()["id"]
        cancel_url = reverse("cancel_reservation", args=[res_id])
        resp = self.client.delete(cancel_url, format="json")
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Reservation.objects.filter(pk=res_id).exists())
        table_id = book_resp.json()["table"]
        self.assertTrue(Table.objects.get(pk=table_id).is_available)

    def test_cancel_invalid_or_other_user(self):
        cancel_url = reverse("cancel_reservation", args=[999])
        resp = self.client.delete(cancel_url, format="json")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

        other = User.objects.create_user(email="other@g.com", password="pw")
        table = Table.objects.filter(is_available=True).first()
        other_res = Reservation.objects.create(
            user=other, table=table, seats=2, cost=2 * self.seat_cost
        )
        cancel_url = reverse("cancel_reservation", args=[other_res.pk])
        resp2 = self.client.delete(cancel_url, format="json")
        self.assertEqual(resp2.status_code, status.HTTP_404_NOT_FOUND)
