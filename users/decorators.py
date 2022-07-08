from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect

def email_verify_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.email_is_verified == False:
            messages.info(request, 'You need to verify your e-mail')
            return redirect('verify-email')
        else:
            return function(request, *args, **kwargs)
    return wrap