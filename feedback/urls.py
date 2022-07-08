from django.urls import path
from . import views

urlpatterns = [
    path('report-business/<slug:slug>/', views.report_business, name='report-business'),
    path('report-product/<slug:slug>/', views.report_product, name='report-product'),
    path('report-business-review/review/', views.report_review, name='report-business-review'),
    path('report-product-review/review/', views.report_product_review, name='report-product-review'),
    path('feedback/contact/', views.contact, name='contact'),
]