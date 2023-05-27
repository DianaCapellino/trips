from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.urls import reverse
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from datetime import date
import json
from .models import User, Destination, Excursion, Hotel, TripData, TripItem, Trip, Comment, SharedUser
from .models import CHILDREN_RANKING_OPTIONS, HOTEL_QUALITY_OPTIONS, SEASONS, INTERESTS, ATTRACTIONS
import random
import math


# Page with the index
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


# Login implementation
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


# Logout implementation
@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


# Register implementation
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


# Creates a new trip
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
        attractions = request.POST.get("attractions", None)
        interests = request.POST.get("interests", None)
        destinations_form = request.POST.get("destinations", None)
        quality = request.POST["quality"]

        # Validations
        if not num_pax or not min_age or not max_age or not num_days:
            return render(request, "argentina/newtrip.html", {
                "message": "All fields must be complete.",
                "hotel_options": HOTEL_QUALITY_OPTIONS,
                "interests": INTERESTS,
                "attractions": ATTRACTIONS,
                "seasons": SEASONS,
                "destinations": Destination.objects.all(),
                "days": list(range(1, 28))
            })
        if int(num_pax) <= 0:
            return render(request, "argentina/newtrip.html", {
                "message": "Number of passengers must be a positive number.",
                "hotel_options": HOTEL_QUALITY_OPTIONS,
                "interests": INTERESTS,
                "attractions": ATTRACTIONS,
                "seasons": SEASONS,
                "destinations": Destination.objects.all(),
                "days": list(range(1, 28))
            })
        if int(min_age) <= 0 or int(max_age) <= 0:
            return render(request, "argentina/newtrip.html", {
                "message": "Age of younger and older passengers must be positive numbers.",
                "hotel_options": HOTEL_QUALITY_OPTIONS,
                "interests": INTERESTS,
                "attractions": ATTRACTIONS,
                "seasons": SEASONS,
                "destinations": Destination.objects.all(),
                "days": list(range(1, 28))
            })
        if int(min_age) > int(max_age):
            return render(request, "argentina/newtrip.html", {
                "message": "Age of younger passenger should be less or equals age of older passenger.",
                "hotel_options": HOTEL_QUALITY_OPTIONS,
                "interests": INTERESTS,
                "attractions": ATTRACTIONS,
                "seasons": SEASONS,
                "destinations": Destination.objects.all(),
                "days": list(range(1, 28))
            })

        # Creates the model of the trip data to get the information
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
        if destinations_form:
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
            "destinations": Destination.objects.all(),
            "days": list(range(1, 28))
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
            if data.attractions_selected:
                if destination.attractions[0] in data.attractions_selected:
                    possible_destinations.append(destination)
            if data.interests_selected:
                if destination.interests[0] in data.interests_selected:
                    possible_destinations.append(destination)
            if visited_destinations:
                if destination in possible_destinations:
                    possible_destinations.remove(destination)
                    

        # Calculates the quantity of destinations
        q_destinations = math.floor(num_days / 3)

        if num_days % 3 == 0:

            # Creates Buenos Aires for 3 nights at the beggining
            create_destination(data, new_trip, 3, left_days, buenos_aires)
            selected_destinations.append(buenos_aires)
            left_days = left_days - 3

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

        elif num_days % 3 == 1:
            
            # Creates Buenos Aires for 4 nights at the beggining
            create_destination(data, new_trip, 4, left_days, buenos_aires)
            selected_destinations.append(buenos_aires)
            left_days = left_days - 4

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
            if hotel.min_age <= 12:
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
            if hotel_age_warning:
                current_item.warning = "Please check ages. No hotel matching"
            current_item.save()
        else:
            
            # Create a list for non used excursions
            nonused_excursions = []
            possible_excursions = Excursion.objects.filter(destination=destination)

            if possible_excursions:
                for excursion in possible_excursions:
                    if excursion not in current_excursions:
                        nonused_excursions.append(excursion)
            else:
                random_excursion = None
            
            # It selects excursion randomly
            if nonused_excursions:
                random_excursion = random.choice(nonused_excursions)
            else:
                random_excursion = None
            
            # Create item for this day in the trip
            current_item = TripItem.objects.create(
                trip=trip,
                dayInTrip=current_day,
                destination=destination,
                excursion=random_excursion,
                hotel=current_hotel
            )
            if hotel_age_warning:
                current_item.warning = "Please check ages. No hotel matching"
            if interest_warning:
                current_item.warning = "Please note there are no services matching interests selected"

            current_item.save()
            current_excursions.append(current_item.excursion)
        current_day = current_day + 1


@login_required
def mytrips(request):
    user_trips = Trip.objects.filter(user=request.user)
    return render(request, "argentina/mytrips.html", {
        "trips": user_trips,
        "shared_trips":request.user.second_user.all()
    })


@login_required
def display_trip(request, trip_id):

    # Gets the trip object
    trip = Trip.objects.get(pk=trip_id)

    # Prepares the list for shared users
    shared_users_list = SharedUser.objects.filter(trip_user=request.user).filter(trip=trip)
    shared_users = []   
    for i in shared_users_list:
        shared_users.append(i.shared_user)

    # Prepares the list for non-shared users
    non_shared_users = []
    for user in User.objects.all():
        if shared_users:
            if user != request.user and user not in shared_users:
                non_shared_users.append(user)
        else:
            non_shared_users = User.objects.exclude(pk=request.user.id)

    # Displays all the details of the trip
    return render(request, "argentina/trip.html", {
        "trip": trip,
        "items": TripItem.objects.filter(trip_id=trip_id),
        "comments": Comment.objects.filter(trip=trip),
        "users": non_shared_users,
        "shared": shared_users
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

        # Takes the trip object with the trip_id
        trip = Trip.objects.get(pk=trip_id)

        # Prepares a list for shared users
        shared_users_list = SharedUser.objects.filter(trip_user=request.user).filter(trip=trip)
        shared_users = []   
        for i in shared_users_list:
            shared_users.append(i.shared_user)

        # Prepares the list for non-shared users
        non_shared_users = []
        for user in User.objects.all():
            if shared_users:
                if user != request.user and user not in shared_users:
                    non_shared_users.append(user)
            else:
                non_shared_users = User.objects.exclude(pk=request.user.id)

        # Get the information from the form
        form_users_id = request.POST["shared-users"]

        # Creates the shared user for the requested users
        for user_id in form_users_id:
            user_object = User.objects.get(pk=user_id)

            if user_object != request.user and user_object in non_shared_users:
                SharedUser.objects.create(
                    trip_user=request.user,
                    shared_user=user_object,
                    trip=trip
                )

        return HttpResponseRedirect(reverse("trip", args=[trip_id]))


@login_required
@csrf_exempt
def trip(request, trip_id):
    
    # Query for trip
    try:
        trip_object = Trip.objects.get(pk=trip_id)
        trip = model_to_dict(trip_object)
    except Trip.DoesNotExist:
        return JsonResponse({"error": "Trip not found."}, status=404)

    # Return trip contents
    if request.method == "GET":
        return JsonResponse(trip, safe=False)

    # Update trip
    elif request.method == "PUT":

        # Check if the user is the owner of the trip and get json information
        if request.user == trip_object.user:
            data = json.loads(request.body)

            # Update information of the trip
            if data.get("name") is not None:
                trip_object.name = data["name"]

            # Save the changes of the trip
            trip_object.save()
            return HttpResponse(status=204)
        else:
            return JsonResponse({"error": "User is not the owner."}, status=404)
    
    # Deletes the trip
    elif request.method == "DELETE":
        trip_object.delete()
        return HttpResponse(status=204)

    # Trip requests must be via GET or PUT or DELETE
    else:
        return JsonResponse({
            "error": "GET or PUT or DELETE request required."
        }, status=400)
    

@login_required
@csrf_exempt
def tripitem(request, tripitem_id):
    
    # Query for trip item
    try:
        tripitem_object = TripItem.objects.get(pk=tripitem_id)
        tripitem = model_to_dict(tripitem_object)
    except TripItem.DoesNotExist:
        return JsonResponse({"error": "Trip Item not found."}, status=404)

    # Return trip contents
    if request.method == "GET":
        return JsonResponse(tripitem, safe=False)

    # Update trip
    elif request.method == "PUT":

        # Check if the user is the owner of the trip and get json information
        if request.user == tripitem_object.trip.user:
            data = json.loads(request.body)

            # Updates day in trip of the trip
            if data.get("dayInTrip") is not None:
                tripitem_object.dayInTrip = data["dayInTrip"]

            # Updates excursion of the trip
            if data.get("excursion") is not None:
                excursion_object = Excursion.objects.get(pk=int(data["excursion"]))
                tripitem_object.excursion = excursion_object

            # Updates hotel of the trip
            if data.get("hotel") is not None:
                hotel_object = Hotel.objects.get(pk=int(data["hotel"]))
                tripitem_object.hotel = hotel_object

            # Save the changes of the trip
            tripitem_object.save()
            return HttpResponse(status=204)
        else:
            return JsonResponse({"error": "User is not the owner."}, status=404)

    # Trip requests must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)
    

# Gets the json response for options to change excursion/hotel
def display_options(request, type, destination_id):

    destination_object = Destination.objects.get(pk=int(destination_id))
    
    if type == "hotel":
        items_list = Hotel.objects.filter(destination=destination_object)
        items = list(items_list.values())
    elif type == "excursion":
        items_list = Excursion.objects.filter(destination=destination_object)
        items = list(items_list.values())
    else:
        return JsonResponse({
            "error": "Type is not recognized."
        }, status=400)

    return JsonResponse(items, safe=False)