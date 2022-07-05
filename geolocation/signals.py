'''from django.db.models.signals import post_save
from mainapp.models import Business
from django.dispatch import receiver
from .models import Geolocation

@receiver(post_save, sender=Business)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Geolocation.objects.create(business=instance)

@receiver(post_save, sender=Business)
def save_profile(sender, instance, **kwargs):
    instance.geolocation.save()'''