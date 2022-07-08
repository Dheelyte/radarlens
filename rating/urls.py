from django.urls import path
from . import views

urlpatterns = [
    path('<str:slug>/reviews/', views.business_reviews, name='business-reviews'),
    path('<str:slug>/rate/', views.business_rating, name='business-rating'),
    path('<str:slug>/rate/edit/', views.edit_business_rating, name='edit-business-rating'),
    path('product/<str:slug>/rate/', views.product_rating, name='product-rating'),
    path('product/<slug:slug>/reviews/', views.product_reviews, name='product-reviews'),
    path('delete-business-review/<int:id>/', views.delete_business_review, name='delete-business-review'),
    path('delete-product-review/<int:id>/', views.delete_product_review, name='delete-product-review'),
]