from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.

class Notification(models.Model):
    content = models.CharField(max_length=500)
    time = models.DateTimeField(auto_now_add=True)
    url = models.URLField(blank=True, null=True)
    lazy_seen = models.BooleanField(default=False)
    seen = models.BooleanField(default=False)
    tag = models.CharField(max_length=100, blank=True)
    receivers = models.ManyToManyField(User)

    def __str__(self):
        return f'Notification {self.id}'