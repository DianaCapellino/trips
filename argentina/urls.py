from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("destinations", views.get_destinations, name="destinations"),
    path("excursions", views.get_excursions, name="excursions"),
    path("hotels", views.get_hotels, name="hotels")
]