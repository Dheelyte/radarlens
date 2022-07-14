from email.policy import default
from operator import mod
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.db.models import Avg
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone
from datetime import time, timedelta
from django.conf import settings
from users.models import IpUser, SavedProduct
from notification.models import Notification
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex 



User = get_user_model() 

class BusinessCategory(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, default="", editable=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        kwargs = {
            'slug': self.slug                                                  # returns slug of the category
        }
        return reverse('business-category', kwargs=kwargs)                              # reverse of url name 'category' in .urls.py

    def save(self, *args, **kwargs):                                           # the save method
        value = self.name                                                      # get the value of the category's name
        self.slug = slugify(value, allow_unicode=True)                          # turns the value of the category's name to a slug
        super().save(*args, **kwargs)


class Business(models.Model):
    location = models.PointField(default=Point(0.0, 0.0, srid=4326))
    show_location = models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, editable=False)
    description = models.CharField(max_length=5000, blank=True)
    opening_hours_from = models.CharField(max_length=20)
    opening_hours_to = models.CharField(max_length=20)
    thumbnail = models.ImageField(upload_to='business_thumbnails', default='DefaultBusinessThumbnail.png')
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=50)
    category = models.ForeignKey(BusinessCategory, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField(User, related_name='followers')
    date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        kwargs = {
            'slug': self.slug,
        }
        return reverse('business-detail', kwargs=kwargs)
    
    def business_visit(self, request, business):
        if request.user != business.user:
            remote_addr = request.META.get('HTTP_X_FORWARDED_FOR')
            if remote_addr:
                address = remote_addr.split(',')[-1].strip()
            else:
                address = request.META.get('REMOTE_ADDR')
            from django.contrib.gis.geoip2 import GeoIP2
            g = GeoIP2()
            location = g.city('197.210.54.179')
            city = location['city']+", "+location['country_name']
            BusinessVisit.objects.create(business=business, remote_address=address, location=city) 

    def business_visits(self):
        return self.businessvisit_set.all().count()

    def monthly_business_visits(self):
        month_ago = timezone.now() - timedelta(days=30)
        return self.businessvisit_set.all().filter(time__gte=month_ago).count()

    def business_call(self, request, business):
        if request.user != business.user:
            BusinessCall.objects.create(business=business, user=request.user)

    def business_calls(self):
        return self.businesscall_set.all().count()

    def monthly_business_calls(self):
        month_ago = timezone.now() - timedelta(days=30)
        return self.businesscall_set.filter(time__gte=month_ago).count()

    def business_direction(self, request, business):
        if request.user != business.user:
            BusinessDirection.objects.create(business=business, user=request.user)
    
    def business_directions(self):
        return self.businessdirection_set.all().count()

    def monthly_business_directions(self):
        month_ago = timezone.now() - timedelta(days=30)
        return self.businessdirection_set.filter(time__gte=month_ago).count()

    def following(self, request):
        if request.user.is_authenticated and request.user != self.user:
            if self.followers.filter(id=request.user.id).exists():
                return True
            else:
                return False

    def rated(self, request):
        if request.user.is_authenticated:
            if self.businessrating_set.filter(user=request.user).exists():
                return True
            else:
                return False

    def rating(self):
        from rating.models import BusinessRating
        rating = BusinessRating.objects.filter(business=self).aggregate(Avg('rating'))
        return rating

    def ratings(self):
        from rating.models import BusinessRating
        ratings = BusinessRating.objects.filter(business=self).count()
        return ratings

    def lat(self):
        return self.location.coords[0]

    def lon(self):
        return self.location.coords[1]

    def save(self, *args, **kwargs):
        self.email = self.user.email
        if not self.id:
            slug = slugify(self.name, allow_unicode=True)
            check = Business.objects.filter(slug=slug)
            if check.exists():
                import random
                number = random.randint(0, 999)
                value = f'{slug}-{number}'
                self.slug = value
            else:
                self.slug = slug 
        super().save(*args, **kwargs)


 

class PostCategory(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, editable=False)

    def __str__(self):
        return self.name


    def get_absolute_url(self):
        kwargs = {
            'slug': self.slug                                                  # returns slug of the category
        }
        return reverse('post-category', kwargs=kwargs)                         # reverse of url name 'category' in .urls.py

    def save(self, *args, **kwargs):                                           # the save method
        if not self.id:
            check = PostCategory.objects.filter(name__iexact=self.name)
            if check.exists():
                value = f'{self.name}-{check.count()}'
            else:
                value = self.name                                               # get the value of the category's name
        self.slug = slugify(value, allow_unicode=True)                          # turns the value of the category's name to a slug
        super().save(*args, **kwargs)

class BusinessPost(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    content = models.CharField(max_length=2000)
    likes = models.ManyToManyField(User, related_name='likes')
    category = models.ForeignKey(PostCategory, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'Id: {self.id}, Business: {self.business.id}'

    def get_absolute_url(self):
        kwargs = {
            'slug': self.business.slug,
            'post_id': self.id
        }
        return reverse('business-posts-detail', kwargs=kwargs)

    def liked(self, user):
        if self.likes.filter(id=user).exists():
            return True
        else:
            return False
    


class BusinessPostComment(models.Model):
    content = models.CharField(max_length=2000)
    datetime = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(BusinessPost, on_delete=models.CASCADE)

    def __str__(self):
        return f'Id: {self.id}, Post: {self.post.id}'


class BusinessVisit(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    remote_address = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now_add=True)

class BusinessCall(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)

class BusinessDirection(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)


class WebsiteVisit(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='website_user', null=True, on_delete=models.CASCADE)
    ipuser = models.ForeignKey(IpUser, related_name='website_ipuser', null=True, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)


class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, editable=False)
    price = models.PositiveIntegerField(blank=True, null=True, default=None)
    currency = models.CharField(max_length=10)
    currency_code = models.CharField(max_length=10)
    description = models.TextField()
    image = models.ImageField(upload_to='products_images', default='ShuttleboostBusiness.png')
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        kwargs = {
            'business': self.business.slug,
            'slug': self.slug,
        }
        return reverse('product-detail', kwargs=kwargs)

    def rated(self, request):
        if request.user.is_authenticated:
            if self.productrating_set.filter(user=request.user).exists():
                return True
            else:
                return False

    def saved(self, request):
        if request.user.is_authenticated:
            if self.savedproduct_set.filter(user=request.user).exists():
                return True
            else:
                return False

    def rating(self):
        from rating.models import ProductRating
        rating = ProductRating.objects.filter(product=self).aggregate(Avg('rating'))
        if rating['rating__avg'] == None:
            return 0
        else:
            return rating['rating__avg']

    def reviews(self):
        reviews = self.productrating_set.order_by('-date_posted')[:10]
        return reviews

    def latest_review(self):
        review = self.productrating_set.order_by('-date_posted').last()
        return review

    def reviews_count(self):
        count = self.productrating_set.count()
        return count

    def save(self, *args, **kwargs):
        if not self.id:
            slug = slugify(self.name, allow_unicode=True)
            check = Product.objects.filter(slug=slug)
            if check.exists():
                import random
                number = random.randint(0, 999)
                value = f'{slug}-{number}'
                self.slug = value
            else:
                self.slug = slug
        super().save(*args, **kwargs)

