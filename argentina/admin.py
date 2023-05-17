from django.contrib import admin
from .models import Destination, Excursion, Hotel, Trip

admin.site.register(Destination)
admin.site.register(Excursion)
admin.site.register(Hotel)
admin.site.register(Trip)