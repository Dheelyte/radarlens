from django.contrib import admin
from .models import Chat, Message

# Register your models here.
admin.site.register(Message)
admin.site.register(Chat)