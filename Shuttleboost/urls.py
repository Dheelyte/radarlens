from itertools import product
from django.contrib import admin, sitemaps
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.sitemaps import views
from django.contrib.sitemaps.views import sitemap
from mainapp.models import BusinessCategory
from sitemaps import BusinessCategorySitemap, BusinessSitemap, ProductSitemap, StaticSitemap
#import debug_toolbar

sitemaps = {
    'business': BusinessSitemap,
    'product': ProductSitemap,
    'businesscategory': BusinessCategorySitemap,
    'static': StaticSitemap
} 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('geolocation.urls')),
    path('', include('users.urls')),
    path('', include('rating.urls')),
    path('', include('notification.urls')),
    path('', include('messaging.urls')),
    path('', include('mainapp.urls')),
    path('', include('feedback.urls')),
    path('sitemap.xml', views.index, {'sitemaps': sitemaps}),
    path('sitemap-<section>.xml', views.sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    #path('debug/', include(debug_toolbar.urls)),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)