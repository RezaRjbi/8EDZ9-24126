from rest_framework import serializers

from .models import Table, Reservation


class BookingSerializer(serializers.Serializer):
    number_of_people = serializers.IntegerField(min_value=1, max_value=10)


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = "__all__"


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = "__all__"
