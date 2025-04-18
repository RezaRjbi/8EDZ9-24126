from rest_framework import serializers

from .models import Table, Reservation


class BookingSerializer(serializers.Serializer):
    number_of_people = serializers.IntegerField(min_value=1)


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = "__all__"
