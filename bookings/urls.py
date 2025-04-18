from django.urls import path

from . import views

urlpatterns = [path("book/", views.BookingView.as_view(), name="booking")]
