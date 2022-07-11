from django.conf import settings
from django.db.models import Q
from mainapp.models import Business, Product
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .decorators import email_verify_required
from .forms import UserLoginForm, UserRegisterForm, UserUpdateForm, UserThumbnailForm
from django.http import JsonResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from .models import SavedProduct

User = get_user_model()


def login_view(request):
    if request.method == "POST":
        next = request.GET.get('next')
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            login(request, user)
            if next:
                return redirect(next)
            else:
                return redirect('account')
    else:
        form = UserLoginForm()
    context = {
        'form': form
    }
    return render(request, 'users/login.html', context)

def signup_view(request):
    if request.method == "POST":
        next = request.GET.get('next')
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            new_user = authenticate(email=user.email, password=password)
            login(request, new_user)
            if next:
                return redirect(next)
            else:
                return redirect('verify-email')
    else:
        form = UserRegisterForm()
    context = {
        'form': form
    }
    return render(request, 'users/signup.html', context)


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
@email_verify_required
def account(request):
    user_update_form = UserUpdateForm(request.POST or None, instance=request.user)
    if user_update_form.is_valid():
        user_update_form.save()
        return redirect('account')
    context = {
        'user_update_form': user_update_form,
    }
    return render(request, 'users/account.html', context)


def followings(request):
    business_following = Business.objects.filter(followers=request.user).order_by('name')
    paginator = Paginator(business_following, 10)
    page = request.GET.get('page')
    try:
        find_post = paginator.page(page)
    except PageNotAnInteger:
        return JsonResponse({"following": "An error occured"})  
    except EmptyPage:
        return JsonResponse({"following": "No more "})
    business_following_list = [{
        "name": business.name,
        "followers": business.followers.count(),
        "url": business.get_absolute_url()
    }for business in find_post]
    if find_post.has_next():
        context = {
        "following": business_following_list,
        "has_next": find_post.has_next(),
        "next": find_post.next_page_number()
    }
    else:
        context = {
            "following": business_following_list,
            "has_next": find_post.has_next(),
        }      
    return JsonResponse(context)


def update_thumbnail(request):
    form = UserThumbnailForm(request.POST, request.FILES, instance=request.user)
    if form.is_valid():
        new = form.save(commit=False)
        new.save()
    else:
        return JsonResponse(form.errors, status=400, safe=False)
    return JsonResponse("Display Picture changed", safe=False)

def following(request):
    if 'page' in request.GET:
        page = request.GET.get('page')
        query_set = Business.objects.filter(followers=request.user).order_by('name')
        paginator = Paginator(query_set, 20)
        try:
            following = paginator.page(page)
        except EmptyPage:
            return JsonResponse("", safe=False)
        following_list = [{
            "name": business.name,
            "image": business.thumbnail.url,
            "category": business.category.name,
            "rating": business.rating(),
            "url": business.get_absolute_url()
        }for business in following]
        context = {
            "following": following_list,
            "has_next": following.has_next()
        }
        return JsonResponse(context)
    else:
        following = Business.objects.filter(followers=request.user).order_by('name')[:20]
        context = {
            'following': following,
            'web_root': settings.WEB_ROOT
        }
    return render(request, 'users/following.html', context)

def save_product(request, slug):
    product = get_object_or_404(Product, slug=slug)
    saved = SavedProduct.objects.filter(product=product, user=request.user)
    if saved.exists():
        SavedProduct.objects.get(product=product, user=request.user).delete()
        return JsonResponse("unsaved", safe=False)
    else:
        SavedProduct.objects.create(product=product, user=request.user)
        return JsonResponse("saved", safe=False)

def saved_products(request):
    if 'page' in request.GET:
        page = request.GET.get('page')
        query_set = SavedProduct.objects.filter(user=request.user).order_by('-date')
        paginator = Paginator(query_set, 15)
        try:
            products = paginator.page(page)
        except EmptyPage:
            return JsonResponse("", safe=False)
        products_list = [{
            "name": product.product.name,
            "currency": product.product.currency,
            "price": product.product.price,
            "image": product.product.image.url,
            "url": product.product.get_absolute_url(),
            "rating": product.product.rating()
        }for product in products]
        context = {
            "products": products_list,
            "has_next": products.has_next()
        }
        return JsonResponse(context)
    else:
        products = SavedProduct.objects.filter(user=request.user).order_by('-date')[:15]
        context = {
            'products': products,
            'web_root': settings.WEB_ROOT
        }
    return render(request, 'users/saved_products.html', context)


@login_required
def verify_email(request):
    if request.method == "POST":
        if request.user.email_is_verified != True:
            current_site = get_current_site(request)
            user = request.user
            email = request.user.email
            subject = "Verify Email"
            message = render_to_string('users/verify_email_message.html', {
                'request': request,
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            email = EmailMessage(
                subject, message, to=[email]
            )
            email.content_subtype = 'html'
            email.send()
            return redirect('verify-email-done')
        else:
            return redirect('login')
    return render(request, 'users/verify_email.html')

@login_required
def verify_email_done(request):
    return render(request, 'users/verify_email_done.html')

@login_required
def verify_email_confirm(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.email_is_verified = True
        user.save()
        messages.success(request, 'Your email has been verified.')
        return redirect('verify-email-complete')   
    else:
        messages.warning(request, 'The link is invalid.')
    return render(request, 'users/verify_email_confirm.html')

@login_required
def verify_email_complete(request):
    return render(request, 'users/verify_email_complete.html')

def privacy_policy(request):
    return render(request, 'users/privacy_policy.html')
