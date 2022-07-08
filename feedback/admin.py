from django.contrib import admin
from .models import ReportBusiness, ReportBusinessReview, ReportBusinessPost, ReportProduct, Contact

# Register your models here.
admin.site.register(Contact)
admin.site.register(ReportBusiness)
admin.site.register(ReportBusinessReview)
admin.site.register(ReportBusinessPost)
admin.site.register(ReportProduct)