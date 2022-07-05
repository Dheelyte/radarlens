from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search, name='search'), 
    path('', views.home, name='home'),   
    path('about/', views.about, name='about'),
    path('create/', views.create_business, name='create-business'),
    path('category/', views.all_business_category, name='all-business-categories'),
    path('category/<str:slug>/', views.business_category, name='business-category'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('<slug:slug>/image/', views.business_thumbnail, name='business-image'),
    path('<slug:slug>/image2/', views.business_thumbnail2, name='business-image2'),
    path('<slug:slug>/home/', views.business_home, name='business-home'),
    path('<slug:slug>/products/', views.business_products, name='business-products'),
    path('<slug:slug>/edit/', views.edit_business, name='business-edit'),
    path('<slug:slug>/add-product/', views.add_product, name='add-product'),
    path('edit-product/<slug:slug>/', views.edit_product, name='edit-product'),
    path('related-products/', views.related_products, name='related-products'),
    path('<slug:slug>/', views.business_detail, name='business-detail'),
    path('delete-business/<slug:slug>/', views.delete_business, name='delete-business'),
    path('delete-business/<slug:slug>/confirm/', views.delete_business_confirm, name='delete-business-confirm'),
    path('delete-product/<slug:slug>/', views.delete_product, name='delete-product'),
    path('delete-product/<slug:slug>/confirm/', views.delete_product_confirm, name='delete-product-confirm'),
    path('<slug:business>/product/<str:slug>/', views.product_detail, name='product-detail'),
    path('service_worker.js', views.service_worker),
    path('manifest.webmanifest', views.webmanifest),
]
handler404 = "mainapp.views.page_not_found_view"