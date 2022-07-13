from django.contrib.sitemaps import Sitemap
from django.contrib import sitemaps
from django.urls import reverse
from mainapp.models import Business, BusinessCategory, Product

class BusinessSitemap(Sitemap):
    changefreq = "always"
    priority = 1

    def items(self):
        return Business.objects.order_by('name')

class ProductSitemap(Sitemap):
    changefreq = "always"
    priority = 1

    def items(self):
        return Product.objects.order_by('name')

class BusinessCategorySitemap(Sitemap):
    changefreq = "always"
    priority = 0.9

    def items(self):
        return BusinessCategory.objects.order_by('name')

class StaticSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return [
            'home',
            'create-business',
            'signup',
            'login',
            'privacy-policy',
        ]
    
    def location(self, item):
        return reverse(item)
