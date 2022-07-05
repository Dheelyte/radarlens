from django.contrib import admin
from .models import (BusinessCategory,
    Business, PostCategory, BusinessPost, BusinessPostComment,
    Product, BusinessVisit, WebsiteVisit, BusinessCall, BusinessDirection
)

# Register your models here.
admin.site.register(BusinessCategory)
admin.site.register(Business)
admin.site.register(Product)
admin.site.register(BusinessVisit)
admin.site.register(WebsiteVisit)
admin.site.register(PostCategory)
admin.site.register(BusinessPost)
admin.site.register(BusinessPostComment)
admin.site.register(BusinessCall)
admin.site.register(BusinessDirection)


