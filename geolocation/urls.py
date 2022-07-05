from django.urls import path
from . import views

urlpatterns = [
    path('geolocation/', views.geolocation, name='geolocation'),
    path('get_category/<int:id>/', views.get_category, name='get-category'),
    path('business-following/', views.business_following, name='business-following'),
    path('<str:slug>/useLocation/', views.use_location, name='use-location'),
    path('<str:slug>/setLocation/', views.business_geolocation, name='business-geolocation')
]