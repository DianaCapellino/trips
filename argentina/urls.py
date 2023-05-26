from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("destinations", views.get_destinations, name="destinations"),
    path("excursions", views.get_excursions, name="excursions"),
    path("hotels", views.get_hotels, name="hotels"),
    path("newtrip", views.newtrip_view, name="newtrip"),
    path("mytrips", views.mytrips, name="mytrips"),
    path("trip/<str:trip_id>", views.display_trip, name="trip"),
    path("trip/<str:trip_id>/add_comment", views.add_comment, name="add_comment"),
    path("trip/<str:trip_id>/share", views.share, name="share"),

    # API Routes
    path("trip/json/<int:trip_id>", views.trip, name="jsontrip"),
    path("trip/tripitem/<int:tripitem_id>", views.tripitem, name="tripitem")
]