from django.contrib.gis import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import Geolocation

@admin.register(Geolocation)
class GeolocationAdmin(OSMGeoAdmin):
    list_display = ('location', 'business')