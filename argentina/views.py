from django.shortcuts import render
from django.http import HttpResponse
from .models import User, Destination, Excursion, Hotel, TripData

def index(request):
    return render(request, "argentina/index.html")


def get_destinations(request):
    return render(request, "argentina/destinations.html", {
        "destinations": Destination.objects.all()
    })


def get_excursions(request):
    return render(request, "argentina/excursions.html", {
        "excursions": Excursion.objects.all()
    })


def get_hotels(request):
    return render(request, "argentina/hotels.html", {
        "hotels": Hotel.objects.all()
    })