from django.contrib import admin
from .models import (BusinessCategory,
    Business, PostCategory, BusinessPost, BusinessPostComment,
    Product, BusinessVisit, BusinessCall, BusinessDirection
)
admin.site.site_header = "RadarLens Admin"
admin.site.site_title = "RadarLens Admin"
admin.site.index_title = "Welcome to the RadarLens Admin"

class BusinessAdmin(admin.ModelAdmin):
    model = Business
    list_display = ("name", "category", "date")
    list_filter = ("date", )
    search_fields = ("name", "email",)
    ordering = ('date',)

class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ("name", "business")
    list_filter = ("date", )
    search_fields = ("name", "email",)
    ordering = ('date',)

class BusinessVisitAdmin(admin.ModelAdmin):
    model = BusinessVisit
    list_display = ("business", "remote_address", "location", "time")
    list_filter = ("time", )
    search_fields = ("business", "remote_address", "location",)
    ordering = ('time',)

# Register your models here.
admin.site.register(BusinessCategory)
admin.site.register(Business, BusinessAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(BusinessVisit, BusinessVisitAdmin)
admin.site.register(PostCategory)
admin.site.register(BusinessPost)
admin.site.register(BusinessPostComment)
admin.site.register(BusinessCall)
admin.site.register(BusinessDirection)


