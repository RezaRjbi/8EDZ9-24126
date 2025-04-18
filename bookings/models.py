from django.db import models
from random import randrange
from functools import partial
from django.contrib.auth import get_user_model


class Table(models.Model):
    seats = models.PositiveIntegerField(default=partial(randrange, 4, 11))
    is_available = models.BooleanField()

    class Meta:
        indexes = [models.Index(fields=["seats"])]


class Reservation(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    seats = models.PositiveIntegerField()
    cost = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=["table_id"])]
