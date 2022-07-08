from .models import Business
from functools import wraps
from django.shortcuts import reverse, get_object_or_404
from django.http import HttpResponseRedirect

def business_owner_required(function):
    @wraps(function)
    def wrap(request, slug, *args, **kwargs):
        business = get_object_or_404(Business, slug=slug)
        if business.user != request.user:
            return HttpResponseRedirect(reverse('business-detail', args=(business.slug,)))
        else:
            return function(request, slug, *args, **kwargs)
    return wrap