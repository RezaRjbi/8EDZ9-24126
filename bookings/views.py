from django.db import transaction
from rest_framework.views import APIView, Response
from rest_framework import permissions, status, generics

from .cruds import reserve_table
from .helpers import calc_total_cost, cal_seats_to_book
from .serializers import BookingSerializer, ReservationSerializer
from .models import Table, Reservation
from drf_spectacular.utils import extend_schema


class BookingView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class: BookingSerializer = BookingSerializer
    SEAT_COST = 5

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        required_seats = serializer.validated_data["number_of_people"]
        least_cost = None
        table_id = None
        booked_seats = None
        available_tables = Table.objects.get_values_list(required_seats, "pk", "seats")
        for pk, seats in available_tables:
            seat_to_book = cal_seats_to_book(required_seats, seats)
            cost = calc_total_cost(seat_to_book, required_seats)
            if least_cost is None or cost < least_cost:
                least_cost = cost
                table_id = pk
                booked_seats = seat_to_book
        if least_cost is None:
            return Response(
                {"detail": "No seats available."}, status=status.HTTP_404_NOT_FOUND
            )
        with transaction.atomic():
            reservation = reserve_table(
                table_id, request.user.id, least_cost, booked_seats
            )
            return Response(
                ReservationSerializer(reservation).data, status=status.HTTP_201_CREATED
            )

    @extend_schema(request=None, responses={200: ReservationSerializer(many=True)})
    def get(self, request):
        return Response(
            ReservationSerializer(
                Reservation.objects.filter(user=request.user).all(), many=True
            ).data,
            status=200,
        )


class RetrieveReservationView(generics.RetrieveAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)


class CancelReservation(generics.DestroyAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def perform_destroy(self, instance: Reservation):
        Table.objects.filter(id=instance.table_id).update(is_available=True)
        super().perform_destroy(instance)
