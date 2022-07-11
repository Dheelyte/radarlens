from django.contrib import admin
from .models import ReportBusiness, ReportBusinessReview, ReportProduct, ReportProductReview, Contact

# Register your models here.
admin.site.register(Contact)
admin.site.register(ReportBusiness)
admin.site.register(ReportBusinessReview)
admin.site.register(ReportProductReview)
admin.site.register(ReportProduct)