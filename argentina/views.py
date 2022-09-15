from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.urls import reverse
import json
from django.forms.models import model_to_dict
from .models import User, Destination, Excursion, Hotel, TripData
from .models import CHILDREN_RANKING_OPTIONS, HOTEL_QUALITY_OPTIONS, SEASONS, INTERESTS, ATTRACTIONS

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


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "argentina/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "argentina/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "argentina/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "argentina/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "argentina/register.html")


def newtrip_view(request):
    return render(request, "argentina/newtrip.html", {
        "hotel_options": HOTEL_QUALITY_OPTIONS,
        "interests": INTERESTS,
        "attractions": ATTRACTIONS,
        "seasons": SEASONS,
        "destinations": Destination.objects.all()
    })


def newtrip_create(request):
    pass