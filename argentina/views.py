from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.urls import reverse
from django.forms.models import model_to_dict
from datetime import date
import json
from .models import User, Destination, Excursion, Hotel, TripData, TripItem, Trip, Comment, SharedUser
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


@login_required
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


@login_required
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


@login_required
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

    # Creates the new trip
    new_trip = Trip.objects.create(
        name=name,
        nights=data.num_days,
        user=data.user,
        start_date=start_date,
        finish_date=finish_date
    )
    new_trip.save()

    left_days = num_days

    # Select Buenos Aires if there is less than 4 days
    if num_days < 4:

        create_destination(data, new_trip, num_days, left_days, buenos_aires)
    
    # Selects Buenos Aires for 2 nights and then randomly
    elif num_days >= 4:
        
        # Empty lists for possible and selected destinations
        possible_destinations = []
        selected_destinations = []

        # Makes the list of visited destinations
        visited_destinations = []

        for destination in Destination.objects.all():
            if destination.id == data.visited_destinations:
                visited_destinations.append(destination)

        # Gets the possible destination according to interests and attractions
        for destination in Destination.objects.all():
            if (destination.attractions[0] in data.attractions_selected
                 or destination.interests[0] in data.interests_selected
                 ) and destination not in visited_destinations:
                possible_destinations.append(destination)

        # Calculates the quantity of destinations
        q_destinations = math.floor(num_days / 3)

        if num_days % 3 == 0:

            # Creates Buenos Aires for 3 nights at the beggining
            create_destination(data, new_trip, 3, left_days, buenos_aires)
            selected_destinations.append(buenos_aires)
            left_days = left_days - 3

            if left_days:
                # Creates other destinations
                for item in range(q_destinations):
                    
                    # Creates an empty list of destinations
                    nonused_destinations = []

                    # Make the list of non used destinations
                    if possible_destinations:
                        for destination in possible_destinations:
                            if destination not in selected_destinations:
                                nonused_destinations.append(destination)
                    else:
                        for destination in Destination.objects.exclude(pk=1):
                            if destination not in selected_destinations:
                                nonused_destinations.append(destination)

                    # It selects any destination except already used destinations
                    if nonused_destinations:
                        current_destination = random.choice(nonused_destinations)
                    else:
                        current_destination = random.choice(Destination.objects.exclude(pk=1))
                    
                    create_destination(data, new_trip, 3, left_days, current_destination)
                    selected_destinations.append(current_destination)
                    left_days = left_days - 3

        elif num_days % 3 == 1:
            
            # Creates Buenos Aires for 4 nights at the beggining
            create_destination(data, new_trip, 4, left_days, buenos_aires)
            selected_destinations.append(buenos_aires)
            left_days = left_days - 4

            if left_days:
                # Creates other destinations
                for item in range(q_destinations):
                    
                    # Creates an empty list of destinations
                    nonused_destinations = []

                    # Make the list of non used destinations
                    if possible_destinations:
                        for destination in possible_destinations:
                            if destination not in selected_destinations:
                                nonused_destinations.append(destination)
                    else:
                        for destination in Destination.objects.exclude(pk=1):
                            if destination not in selected_destinations:
                                nonused_destinations.append(destination)

                    # It selects any destination except already used destinations
                    if nonused_destinations:
                        current_destination = random.choice(nonused_destinations)
                    else:
                        current_destination = random.choice(Destination.objects.exclude(pk=1))

                    create_destination(data, new_trip, 3, left_days, current_destination)
                    selected_destinations.append(current_destination)
                    left_days = left_days - 3
        else:

            # Creates Buenos Aires for 3 nights at the beggining
            create_destination(data, new_trip, 3, left_days, buenos_aires)
            selected_destinations.append(buenos_aires)
            left_days = left_days - 3

            
            # Creates Iguazu for 2 nights at the beggining
            create_destination(data, new_trip, 2, left_days, iguazu)
            selected_destinations.append(iguazu)
            left_days = left_days - 2

            if left_days:
                # Creates other destinations
                for item in range(q_destinations-1):
                    
                    # Creates an empty list of destinations
                    nonused_destinations = []

                    # Make the list of non used destinations
                    if possible_destinations:
                        for destination in possible_destinations:
                            if destination not in selected_destinations:
                                nonused_destinations.append(destination)
                    else:
                        for destination in Destination.objects.exclude(pk=1):
                            if destination not in selected_destinations:
                                nonused_destinations.append(destination)

                    # It selects any destination except already used destinations
                    if nonused_destinations:
                        current_destination = random.choice(nonused_destinations)
                    else:
                        current_destination = random.choice(Destination.objects.exclude(pk=1))
                    
                    create_destination(data, new_trip, 3, left_days, current_destination)
                    selected_destinations.append(current_destination)
                    left_days = left_days - 3

@login_required
def create_destination(data, trip, days, left_days, destination):

    # Setting all warnings as desactivated
    hotel_age_warning = False
    interest_warning = False

    # Creates an empty list for possible hotels
    possible_hotels = []

    # First filtered hotel selection by quality and destination
    first_filtered_hotels = Hotel.objects.filter(destination=destination).filter(hotel_quality=data.hotel_quality_selected)

    # Makes a list of hotels matching ages
    if data.are_children:
        for hotel in first_filtered_hotels:
            if hotel.min_age >= 12:
                possible_hotels.append(hotel)

        # If any hotel matches, takes all hotels but set a warning
        if not possible_hotels:
            for hotel in first_filtered_hotels:
                possible_hotels.append(hotel)
                hotel_age_warning = True
    else:
        for hotel in first_filtered_hotels:
            possible_hotels.append(hotel)

    # Select hotel according to the quality selected
    current_hotel = random.choice(possible_hotels)
    
    # List of excursions to keep track and avoid repeating excursions
    current_excursions = []
    
    # Keep track of the day
    current_day = int(data.num_days) - left_days + 1

    # Create item for each day
    for day in range(days):

        # If it is the last day it will not have excursion nor hotel
        if current_day == int(data.num_days):
            current_item = TripItem.objects.create(
                trip=trip,
                dayInTrip=current_day,
                destination=destination,
                excursion=None,
                hotel=None
            )
            current_item.save()

        # If it is the last day in the destination will not have excursion
        elif day == 0:
            current_item = TripItem.objects.create(
                trip=trip,
                dayInTrip=current_day,
                destination=destination,
                excursion=None,
                hotel=current_hotel
            )
            current_item.save()
        else:
            # Check all items in the trip
            all_items = TripItem.objects.filter(trip=trip)
            
            # Create a list for non used excursions
            nonused_excursions = []
            if all_items:
                for excursion in Excursion.objects.filter(destination=destination):
                    if excursion in current_excursions:
                        pass
                    else:
                        nonused_excursions.append(excursion)
            
            # It selects excursion randomly
            if nonused_excursions:
                random_excursion = random.choice(nonused_excursions)
            else:
                random_excursion = random.choice(Excursion.objects.filter(destination=destination))
            
            # Create item for this day in the trip
            current_item = TripItem.objects.create(
                trip=trip,
                dayInTrip=current_day,
                destination=destination,
                excursion=random_excursion,
                hotel=current_hotel
            )

            current_item.save()
            current_excursions.append(current_item.excursion)
        
        # Sets the warnings if they are activated
        if hotel_age_warning:
            warning = "Please check ages. No hotel matching"
        if interest_warning:
            warning = "Please note there are no services matching interests selected"
        current_day = current_day + 1


@login_required
def mytrips(request):
    user_trips = Trip.objects.filter(user=request.user)
    return render(request, "argentina/mytrips.html", {
        "trips": user_trips
    })


@login_required
def display_trip(request, trip_id):
    trip = Trip.objects.get(pk=trip_id)
    user_id = request.user.id

    return render(request, "argentina/trip.html", {
        "trip": trip,
        "items": TripItem.objects.filter(trip_id=trip_id),
        "comments": Comment.objects.filter(trip=trip),
        "users": User.objects.exclude(pk=user_id),
        "shared": SharedUser.objects.filter(trip_user=request.user).filter(trip=trip)
    })


def add_comment(request, trip_id):
    
    # When submitting the comment
    if request.method == "POST":

        # Get the information of the comment provided and trip_id and user from the page
        new_comment = request.POST["comment"]
        trip = Trip.objects.get(pk=trip_id)
        user = request.user

        # It creates the comment and redirect to the trip page
        comment = Comment(user=user, trip=trip, comment=new_comment)
        comment.save()

        return HttpResponseRedirect(reverse("trip", args=[trip_id]))


def share(request, trip_id):

    # When submitting the form
    if request.method == "POST":

        shared_users = request.POST["shared-users"]

        # Get the information from the form
        for user in shared_users:
            trip = Trip.objects.get(pk=trip_id)
            user_object = User.objects.get(pk=user)

        new_shareduser = SharedUser.objects.create(
            trip_user=request.user,
            shared_user=user_object,
            trip=trip
        )

        return HttpResponseRedirect(reverse("trip", args=[trip_id]))

@login_required
def trips(request):
    trips = Trip.objects.filter(user=request.user)
    return JsonResponse([trip.serialize() for trip in trips], safe=False)


@login_required
def trip(request, trip_id):
    return HttpResponseRedirect(reverse("mytrips"))