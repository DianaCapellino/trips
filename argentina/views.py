from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.urls import reverse
from django.forms.models import model_to_dict
from datetime import date
import json
from .models import User, Destination, Excursion, Hotel, TripData, TripExcursions, TripDestination, Trip, Comment
from .models import CHILDREN_RANKING_OPTIONS, HOTEL_QUALITY_OPTIONS, SEASONS, INTERESTS, ATTRACTIONS
import random
import math


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
            hotel_quality_selected=quality
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

        create_trip(new_trip)

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


def create_trip(data):
    # Creating name of the trip
    passenger_name = data.user.username
    passenger_num = data.num_pax
    name = passenger_name + " x " + passenger_num

    # Creating start and finish dates
    today = date.today()
    current_month = 0
    travel_year = 0
    for season in SEASONS:
        if int(data.travel_season) == season[0]:
            if current_month <= today.month:
                travel_year = int(today.year + 1)
            else:
                travel_year = int(today.year)
        current_month = current_month + 1
    
    start_date = date(travel_year, int(data.travel_season), 1)
    finish_date = date(travel_year, int(data.travel_season), 1 + int(data.num_days))
    
    num_days = int(data.num_days)
    # Empty list of destinations
    tripDestinations = []
    
    # Objects for each destination
    buenos_aires = Destination.objects.get(id=1)
    el_calafate = Destination.objects.get(id=2)
    iguazu = Destination.objects.get(id=3)
    lakes = Destination.objects.get(id=4)
    ushuaia = Destination.objects.get(id=5)
    mendoza = Destination.objects.get(id=6)
    northwest = Destination.objects.get(id=7)
    peninsula_valdes = Destination.objects.get(id=8)
    wetlands = Destination.objects.get(id=9)

    if num_days < 4:
        
        destinationExcursions = []

        if num_days > 1:
            for day in range(num_days-1):
                current_excursion = TripExcursions.objects.create(
                    dayInTrip = day,
                    excursion = random.choice(Excursion.objects.filter(destination=buenos_aires))
                )
                destinationExcursions.append(current_excursion)
                
        current_destination = TripDestination.objects.create(
            destination = buenos_aires,
            nights = num_days,
            excursions = TripExcursions.objects.create(
                dayInTrip = day,
                excursion = random.choice(Excursion.objects.filter(destination=buenos_aires))
            ),
            hotel = random.choice(Hotel.objects.filter(destination=buenos_aires).filter(hotel_quality=data.hotel_quality_selected)),
            orderInTrip = 1
        )
        current_destination.save()

        new_trip = Trip.objects.create(
            name=name,
            nights=data.num_days,
            user=data.user,
            start_date=start_date,
            finish_date=finish_date
        )
        new_trip.destinations.add(TripDestination.objects.get(pk=13))
        new_trip.save()

    elif int(data.num_days) >= 4:
        destinationExcursions = []
        destinationExcursions.append(TripExcursions.objects.create(
            dayInTrip = 1,
            excursion = random.choice(Excursion.objects.filter(destination=buenos_aires))
        ))
        destinationExcursions.append(TripExcursions.objects.create(
            dayInTrip = 2,
            excursion = random.choice(Excursion.objects.filter(destination=buenos_aires))
        ))
        q_destinations = math.floor(int(data.num_days) / 3)
        current_trip_destination = TripDestination(
            destination = buenos_aires,
            nights = 3,
            excursions = TripExcursions.objects.create(
                dayInTrip = 1,
                excursion = random.choice(Excursion.objects.filter(destination=buenos_aires))
            ),
            hotel = random.choice(Hotel.objects.filter(destination=buenos_aires).filter(hotel_quality=data.hotel_quality_selected)),
            orderInTrip = 1
        )
        current_trip_destination.save()
        tripDestinations.append(current_trip_destination)
        
        current_order = 1
        left_nights = int(data.num_days)
        for item in range(q_destinations-1):
            current_nights = 3
            if left_nights >= 3:
                current_nights = 3
            else:
                current_nights = left_nights
            
            current_destination = random.choice(Destination.objects.all())
            
            destinationExcursions = []

            if current_nights > 1:
                for day in range(current_nights-1):
                    destinationExcursions.append(TripExcursions.objects.create(
                        dayInTrip = day,
                        excursion = random.choice(Excursion.objects.filter(destination=current_destination))
                    ))    
            current_trip_destination = TripDestination(
                destination = current_destination,
                nights = current_nights,
                excursions = TripExcursions.objects.create(
                    dayInTrip = 1,
                    excursion = random.choice(Excursion.objects.filter(destination=buenos_aires))
                ),
                hotel = random.choice(Hotel.objects.filter(destination=current_destination).filter(hotel_quality=data.hotel_quality_selected)),
                orderInTrip = current_order + 1
            )
            current_trip_destination.save()  
            tripDestinations.append(current_trip_destination)

            current_order = current_order + 1
            left_nights = left_nights - 3


def mytrips(request):
    return render(request, "argentina/mytrips.html", {
        "trips": Trip.objects.filter(user=request.user)
    })


@login_required
def trips(request):
    trips = Trip.objects.filter(user=request.user)
    return JsonResponse([trip.serialize() for trip in trips], safe=False)


@login_required
def trip(request, trip_id):
    return HttpResponseRedirect(reverse("mytrips"))