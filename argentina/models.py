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
    (1, "January"),
    (2, "February"),
    (3, "March"),
    (4, "April"),
    (5, "May"),
    (6, "June"),
    (7, "July"),
    (8, "August"),
    (9, "September"),
    (10, "October"),
    (11, "November"),
    (12, "December")
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
    attractions = MultiSelectField(choices=ATTRACTIONS, max_length=500)
    interests = MultiSelectField(choices=INTERESTS, max_length=500)
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
    attractions_selected = MultiSelectField(choices=ATTRACTIONS, max_length=500, blank=True, null=True)
    interests_selected = MultiSelectField(choices=INTERESTS, max_length=500, blank=True, null=True)
    travel_season = MultiSelectField(choices=SEASONS, max_length=500)
    visited_destinations = models.ManyToManyField(Destination, related_name="visited", blank=True)
    hotel_quality_selected = models.CharField(choices=HOTEL_QUALITY_OPTIONS, max_length=10)


class Excursion(models.Model):
    class Meta:
        ordering = ('name',)

    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name="excursions")
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1500)
    pic1_url = models.CharField(max_length=500)
    pic2_url = models.CharField(max_length=500)
    pic3_url = models.CharField(max_length=500)
    season = MultiSelectField(choices=SEASONS, max_length=500)
    interests = MultiSelectField(choices=INTERESTS, max_length=500)
    min_age = models.PositiveSmallIntegerField()
    max_age = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.name}"
    
    def serialize(self):
        return {
            "id": self.id,
            "destination_id": self.destination.id,
            "name": self.name
        }


class Hotel(models.Model):
    class Meta:
        ordering = ('name',)

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
    
    def serialize(self):
        return {
            "id": self.id,
            "destination_id": self.destination.id,
            "name": self.name
        }


class Trip(models.Model):
    class Meta:
        ordering = ('-id',)
        
    name = models.CharField(max_length=200)
    nights = models.PositiveSmallIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="trip_user")
    start_date = models.DateTimeField(default=django.utils.timezone.now, verbose_name='start_date')
    finish_date = models.DateTimeField(default=django.utils.timezone.now, verbose_name='finish_date')

    def __str__(self):
        return f"{self.name} created by {self.user}"
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "nights": self.nights,
            "user": self.user.username,
            "start_date": self.start_date,
            "finish_date": self.finish_date
        }


class TripItem(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="items")
    dayInTrip = models.PositiveSmallIntegerField()
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name="destination_item")
    excursion = models.ForeignKey(Excursion, on_delete=models.CASCADE, blank=True, null=True, related_name="excursion_item")
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, blank=True, null=True, related_name="hotel_item")
    warning = models.CharField(blank=True, max_length=500)

    def serialize(self):
        return {
            "id": self.id,
            "trip": self.trip.id,
            "dayInTrip": self.dayInTrip,
            "destination": self.destination.name,
            "destination_id": self.destination.id,
            "excursion": self.excursion.name,
            "hotel": self.hotel.name,
            "warning": self.warning
        }


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_users")
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="comment_trip")
    comment = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now=True, verbose_name='comment_date')

    def __str__(self):
        return f"{self.comment} (by: {self.user})"


class SharedUser(models.Model):
    trip_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="first_user")
    shared_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="second_user")
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="shared_trip")