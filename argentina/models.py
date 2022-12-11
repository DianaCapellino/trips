from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import ModelForm
from django.conf import settings
from multiselectfield import MultiSelectField
import django.utils.timezone


ATTRACTIONS = [
    ("CITY", "City"),
    ("FALLS", "Falls"),
    ("MOUNTAINS", "Mountains"),
    ("COUNTRYSIDE", "Countryside"),
    ("GLACIERS", "Glaciers"),
    ("WILDLIFE", "Wildlife")
]


INTERESTS = [
    ("FOOD", "Food"),
    ("MUSIC", "Music"),
    ("ART", "Art"),
    ("TREKKING", "Trekking"),
    ("ACTIVE", "Active Activities"),
    ("RELAXING", "Relaxing"),
    ("LANDSCAPES", "Landscapes"),
    ("NATURE", "Nature"),
    ("CULTURE", "Culture")
]


SEASONS = [
    ("JANUARY", "January"),
    ("FEBRUARY", "February"),
    ("MARCH", "March"),
    ("APRIL", "April"),
    ("MAY", "May"),
    ("JUNE", "June"),
    ("JULY", "July"),
    ("AUGUST", "August"),
    ("SEPTEMBER", "September"),
    ("OCTOBER", "October"),
    ("NOVEMBER", "November"),
    ("DECEMBER", "December")
]


CHILDREN_RANKING_OPTIONS = [
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
    ("5", "5"),
]


HOTEL_QUALITY_OPTIONS = [
    ("3", "3"),
    ("4", "4"),
    ("5", "5"),
]


class User(AbstractUser):

    def __str__(self):
        return f"{self.username}"


class Destination(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    pic1_url = models.CharField(max_length=500)
    pic2_url = models.CharField(max_length=500)
    pic3_url = models.CharField(max_length=500)
    attractions = MultiSelectField(choices=ATTRACTIONS)
    interests = MultiSelectField(choices=INTERESTS)
    min_nights = models.PositiveSmallIntegerField()
    max_nights = models.PositiveSmallIntegerField()
    children_ranking = models.CharField(choices=CHILDREN_RANKING_OPTIONS, max_length=10)

    def __str__(self):
        return f"{self.name}"


class TripData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner_user")
    are_children = models.BooleanField(default=False)
    max_age = models.PositiveSmallIntegerField()
    num_pax = models.PositiveSmallIntegerField()
    num_days = models.PositiveSmallIntegerField()
    attractions_selected = MultiSelectField(choices=ATTRACTIONS)
    interests_selected = MultiSelectField(choices=INTERESTS)
    travel_season = MultiSelectField(choices=SEASONS)
    visited_destinations = models.ManyToManyField(Destination, related_name="visited", blank=True)
    hotel_quality_selected = models.CharField(choices=HOTEL_QUALITY_OPTIONS, max_length=10)

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.name,
            "are_children": self.are_children,
            "max_age": self.max_age,
            "num_pax": self.num_pax,
            "num_days": self.num_days,
            "attractions_selected": [self.attractions.all()],
            "interests_selected": [self.interests.all()],
            "travel_season": self.travel_season,
            "visited_destinations": [self.visited_destinations.all()],
            "hotel_quality_selected": self.hotel_quality_selected
        }


class Excursion(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name="excursions")
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1500)
    pic1_url = models.CharField(max_length=500)
    pic2_url = models.CharField(max_length=500)
    pic3_url = models.CharField(max_length=500)
    season = MultiSelectField(choices=SEASONS)
    interests = MultiSelectField(choices=INTERESTS)
    min_age = models.PositiveSmallIntegerField()
    max_age = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.name}"


class Hotel(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name="properties")
    hotel_quality = models.CharField(choices=HOTEL_QUALITY_OPTIONS, max_length=10)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=800)
    pic1_url = models.CharField(max_length=500)
    pic2_url = models.CharField(max_length=500)
    pic3_url = models.CharField(max_length=500)
    min_age = models.PositiveSmallIntegerField()
    max_age = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.name}"


class TripExcursions(models.Model):
    dayInTrip = models.PositiveSmallIntegerField()
    excursion = models.ForeignKey(Excursion, on_delete=models.CASCADE, related_name="destination_excursions")


class TripDestination(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name="destination")
    nights = models.PositiveSmallIntegerField()
    excursions = models.ForeignKey(TripExcursions, on_delete=models.CASCADE, related_name="destination_excursions")
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="stay")
    orderInTrip = models.PositiveSmallIntegerField()


class Trip(models.Model):
    name = models.CharField(max_length=200)
    destinations = models.ManyToManyField(TripDestination, related_name="trip_destinations")
    nights = models.PositiveSmallIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="trip_user")
    shared_with = models.ManyToManyField(User, related_name="companions_trip")
    start_date = models.DateTimeField(default=django.utils.timezone.now, verbose_name='start_date')
    finish_date = models.DateTimeField(default=django.utils.timezone.now, verbose_name='finish_date')

    def __str__(self):
        return f"{self.name} created by {self.user}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_users")
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="comment_trip")
    comment = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now=True, verbose_name='comment_date')

    def __str__(self):
        return f"{self.comment} (by: {self.user})"