from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Geolocation
from .forms import MyGeoForm
from mainapp.models import Business, BusinessCategory, BusinessPost
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from notification.models import Notification
from django.conf import settings
from django.core import serializers



def geolocation(request):
    from django.contrib.gis.geoip2 import GeoIP2
    g = GeoIP2()
    remote_addr = request.META.get('HTTP_X_FORWARDED_FOR')
    if remote_addr:
        address = remote_addr.split(',')[-1].strip()
    else:
        address = request.META.get('REMOTE_ADDR')
    location = (g.country('197.210.54.179'))
    print(g.country('197.210.54.179'))
    return JsonResponse(location, safe=False)


def business_following(request):
    following = BusinessPost.objects.filter(business__followers=request.user)[:5]
    businesses = [{
        "name": business.business.name,
        "category": business.category.name,
        "ccontent": business.content,
        "slug": business.get_absolute_url(),
    }for business in following]
    return JsonResponse(businesses, safe=False)


def get_category(request, id):
    latitude = float(request.GET.get('latitude'))
    longitude = float(request.GET.get('latitude'))
    location = Point(longitude, latitude, srid=4326)
    category = get_object_or_404(BusinessCategory, id=id).name
    businesses_qs = Geolocation.objects.filter(business__category__id=id).annotate(distance=Distance(location, 'location')).order_by('distance')
    businesses = [{
        "name": business.business.name,
        "thumbnail": business.business.thumbnail.url,
        "category": business.business.category.name,
        "slug": business.business.get_absolute_url(),
        "rating": business.business.rating()["rating__avg"],
    }for business in businesses_qs]
    for b in businesses_qs:
        print(b.business.name, b.distance)
    context = {
        "category": category,
        "businesses": businesses
    }
    return JsonResponse(context)


'''def x(request):
    location = Point(longitude, latitude, srid=4326)
    general = Geolocation.objects.filter(business__category__id=1).annotate(distance=Distance(location, 'location')).order_by('distance')
    catering = Geolocation.objects.filter(business__category__id=2).annotate(distance=Distance(location, 'location')).order_by('distance')
    confectionery = Geolocation.objects.filter(business__category__id=3).annotate(distance=Distance(location, 'location')).order_by('distance')
    

    businesses = [{
        "name": business.business.name,
        "thumbnail": business.business.thumbnail.url,
        "category": business.business.category.name,
        "slug": business.business.get_absolute_url(),
        "rating": business.business.rating()
    }for business in general]
    for p in general:
        print(p.business.name, p.distance)
    return JsonResponse(businesses, safe=False)'''


def get_businesses(request, category):
    location = request.POST.get('current_location')
    businesses = Geolocation.objects.filter(business__category__slug=category).annotate(distance=Distance(location, 'location')).order_by('distance')
    return JsonResponse({})


def ip_geolocation(request):
    remote_addr = request.META.get('HTTP_X_FORWARDED_FOR')
    if remote_addr:
        address = remote_addr.split(',')[-1].strip()
    else:
        address = request.META.get('REMOTE_ADDR')
        
def use_location(request, slug):
    if request.method == "POST":
        business = get_object_or_404(Business, slug=slug)
        latitude = float(request.POST.get('latitude'))
        longitude = float(request.POST.get('longitude'))
        location = Point(longitude, latitude, srid=4326)
        business.location = location
        business.save()
        return JsonResponse("success", safe=False)

def business_geolocation(request, slug):
    business = get_object_or_404(Business, slug=slug)
    if request.method == "POST":
        form = MyGeoForm(request.POST, instance=business)
        if form.is_valid():
            form.save()
            notification = Notification.objects.create(
                content=f"You just changed {business.name}'s location",
                url=settings.WEB_ROOT+'/'+business.slug+'/',
                tag=business.name
            )
            notification.receivers.add(request.user)
    else:
        form = MyGeoForm()
    context = {
        'form': form,
        'business': business
    }
    return render(request, 'geolocation/business_geolocation.html', context)