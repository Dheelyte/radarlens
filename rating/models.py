from django.db import models
from django.contrib.auth import get_user_model
from mainapp.models import Business, Product

User = get_user_model()


class BusinessRating(models.Model):
    rating = models.IntegerField(default=0)
    content = models.TextField(blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class ProductRating(models.Model):
    rating = models.IntegerField(default=0)
    content = models.TextField(blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)