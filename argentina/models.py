from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import ModelForm
from django.conf import settings
from multiselectfield import MultiSelectField


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
    ("RELAXING", "Relaxing")
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
    (1, "1"),
    (2, "2"),
    (3, "3"),
    (4, "4"),
    (5, "5"),
]


HOTEL_QUALITY_OPTIONS = [
    (3, "3"),
    (4, "4"),
    (5, "5"),
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
    atractions = MultiSelectField(choices=ATTRACTIONS)
    interests = MultiSelectField(choices=INTERESTS)
    min_nights = models.PositiveSmallIntegerField()
    max_nights = models.PositiveSmallIntegerField()
    children_ranking = MultiSelectField(choices=CHILDREN_RANKING_OPTIONS)

    def __str__(self):
        return f"{self.name}"


class TripData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner_user")
    name = models.CharField(max_length=100)
    are_children = models.BooleanField(default=False)
    max_age = models.PositiveSmallIntegerField()
    num_pax = models.PositiveSmallIntegerField()
    num_days = models.PositiveSmallIntegerField()
    atractions_selected = MultiSelectField(choices=ATTRACTIONS)
    interests_selected = MultiSelectField(choices=INTERESTS)
    travel_season = MultiSelectField(choices=SEASONS)
    visited_destinations = models.ManyToManyField(Destination, related_name="visited")
    hotel_quality_selected = MultiSelectField(choices=HOTEL_QUALITY_OPTIONS)

    def __str__(self):
        return f"{self.name}"


class Excursion(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name="excursions")
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=800)
    picture1 = models.CharField(max_length=500)
    pic2_url = models.CharField(max_length=500)
    pic3_url = models.CharField(max_length=500)
    season = MultiSelectField(choices=SEASONS)
    atractions = MultiSelectField(choices=ATTRACTIONS)
    interests = MultiSelectField(choices=INTERESTS)
    min_age = models.PositiveSmallIntegerField()
    max_age = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.name}"


class Hotel(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name="properties")
    hotel_quality = MultiSelectField(choices=HOTEL_QUALITY_OPTIONS)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=800)
    picture1 = models.CharField(max_length=500)
    pic2_url = models.CharField(max_length=500)
    pic3_url = models.CharField(max_length=500)
    min_age = models.PositiveSmallIntegerField()
    max_age = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.name}"