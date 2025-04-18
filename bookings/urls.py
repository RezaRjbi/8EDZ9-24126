from django.urls import path

from . import views

urlpatterns = [
    path("book/", views.BookingView.as_view(), name="reservations"),
    path("book/<int:pk>/", views.RetrieveReservationView.as_view(), name="reservation"),
    path(
        "cancel/<int:pk>/", views.CancelReservation.as_view(), name="cancel_reservation"
    ),
]
