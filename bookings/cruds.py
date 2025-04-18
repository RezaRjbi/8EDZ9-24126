from typing import Iterator, Sequence

from rest_framework.exceptions import APIException

from .models import Table, Reservation


def reserve_table(table_id: int, user_id: int, cost: int, seats: int) -> Reservation:
    table_has_been_booked = Table.objects.filter(pk=table_id, is_available=True).update(
        is_available=False
    )
    if not table_has_been_booked:
        raise APIException("No seats available")
    return Reservation.objects.create(
        user_id=user_id,
        table_id=table_id,
        cost=cost,
        seats=seats,
    )
