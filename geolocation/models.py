from django.contrib.gis.db import models
from mainapp.models import Business
from django.contrib.gis.geos import Point

# Create your models here.
class Geolocation(models.Model):
    location = models.PointField(default=Point(0.0, 0.0, srid=4326))
    business = models.OneToOneField(Business, on_delete=models.CASCADE)

    def __str__(self):
        return self.business.name

    def get_location(self, request):
        str_latitude = request.POST.get('latitude')
        str_longitude = request.POST.get('longitude')
        print('strings', str_latitude, str_longitude)
        if str_latitude == "" or str_longitude == "":
            from django.contrib.gis.geoip2 import GeoIP2
            g = GeoIP2()
            remote_addr = request.META.get('HTTP_X_FORWARDED_FOR')
            if remote_addr:
                address = remote_addr.split(',')[-1].strip()
            else:
                address = request.META.get('REMOTE_ADDR')
            location = (g.geos('102.91.5.226'))
            print('location', location)
        else:
            longitude = float(str_latitude)
            latitude = float(str_longitude)
            location = Point(longitude, latitude, srid=4326)
            print('geo', latitude, longitude)
        return location
