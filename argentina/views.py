from django.shortcuts import render
from django.http import HttpResponse
from .models import User, Destination, Excursion, Hotel, TripData

def index(request):
    return render(request, "argentina/index.html", {
        "destinations": Destination.objects.all()
    })