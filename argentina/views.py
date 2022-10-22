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


# Page with the list of destinations
def get_destinations(request):
    return render(request, "argentina/destinations.html", {
        "destinations": Destination.objects.all()
    })


# Page with the list of excursions
def get_excursions(request):
    return render(request, "argentina/excursions.html", {
        "excursions": Excursion.objects.all()
    })


# Page with the list of hotels
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

    # If the user submit the form
    if request.method == "POST":

        # Takes the information in the form
        num_pax = request.POST["passengers"]
        min_age = request.POST["min_age"]
        max_age = request.POST["max_age"]
        num_days = request.POST["days"]
        season = request.POST["season"]
        attractions = request.POST["attractions"]
        interests = request.POST["interests"]
        destinations_form = request.POST["destinations"]
        quality = request.POST["quality"]

        # Create the model of the trip data to get the information
        new_trip = TripData.objects.create(
            user=request.user,
            num_pax=num_pax,
            max_age=max_age,
            num_days=num_days,
            travel_season=season,
            attractions_selected=attractions,
            interests_selected=interests,
            hotel_quality_selected=quality,
        )

        # Add each destination to the information of the trip data
        for destination_id in destinations_form:
            destination = Destination.objects.get(id=destination_id)
            new_trip.visited_destinations.add(destination)

        # If the younger passenger is less than 12, there are children
        if int(min_age) < 12:
            new_trip.are_children = True

        # Save the latest changes
        new_trip.save()

        # Redirect to My Trips section
        return HttpResponseRedirect(reverse("mytrips"))

    # Display the form if viewing the page
    else:
        return render(request, "argentina/newtrip.html", {
            "hotel_options": HOTEL_QUALITY_OPTIONS,
            "interests": INTERESTS,
            "attractions": ATTRACTIONS,
            "seasons": SEASONS,
            "destinations": Destination.objects.all()
        })


def mytrips(request):
    return render(request, "argentina/mytrips.html")