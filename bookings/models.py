from typing import Iterator

from django.db import models
from random import randrange
from functools import partial
from django.contrib.auth import get_user_model


class TableManager(models.Manager):
    def get_values_list(
        self, required_seats: int, *fields: str, as_iterator: bool = True
    ) -> list[tuple[int, int]] | Iterator[tuple[int, int]]:
        query = self.filter(is_available=True, seats__gte=required_seats).values_list(
            *fields
        )
        return query.iterator() if as_iterator else query.all()


class Table(models.Model):
    seats = models.PositiveIntegerField(default=partial(randrange, 4, 11))
    is_available = models.BooleanField()

    objects = TableManager()

    class Meta:
        indexes = [models.Index(fields=["seats"])]

    def __str__(self):
        return (
            f"{self.seats} seats table ({'' if self.is_available else 'not'} available)"
        )


class Reservation(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    seats = models.PositiveIntegerField()
    cost = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=["table_id"]), models.Index(fields=["user_id"])]

    def __str__(self):
        return f"Reservation for user: {self.user_id} for table: {self.table_id}"
