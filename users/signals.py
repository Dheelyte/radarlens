from django.db.models.signals import pre_save
from .models import CustomUser
from django.dispatch import receiver

@receiver(pre_save, sender=CustomUser)
def unverify_email(sender, instance, **kwargs):
    try:
        obj = sender.objects.get(slug=instance.slug)
    except sender.DoesNotExist:
        pass
    else:
        if not obj.email == instance.email:
            instance.email_is_verified = False
