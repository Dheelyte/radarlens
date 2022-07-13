from dataclasses import field
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.core import paginator
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.contrib.gis.db.models.functions import Distance
from users.decorators import email_verify_required
from .decorators import business_owner_required
from .models import  Business, BusinessCategory, Product, WebsiteVisit, BusinessVisit, BusinessPost, BusinessPostComment
from users.models import IpUser
from geolocation.models import Geolocation
from notification.models import Notification
from rating.models import BusinessRating, ProductRating
from .forms import BusinessCreationForm, BusinessThumbnailForm, BusinessThumbnailForm2, ProductForm, BusinessEditForm, BusinessPersonalInfoEditForm, CreateBusinessPost, BusinessPostCommentForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, response
from django.core import serializers
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.gis.geos import Point
from django.contrib.humanize.templatetags.humanize import naturalday
import json


def currency(request):
    from django.contrib.gis.geoip2 import GeoIP2
    g = GeoIP2()
    remote_addr = request.META.get('HTTP_X_FORWARDED_FOR')
    if remote_addr:
        address = remote_addr.split(',')[-1].strip()
    else:
        address = request.META.get('REMOTE_ADDR')
    if settings.DEBUG == True:
        country = g.country_code(settings.DEV_GEOLOCATION_IP)
    else:
        country = g.country_code(address)
    f = open('static/json/currency.json', encoding="utf8")
    data = json.load(f)
    for keyval in data:
        if country == keyval['isoAlpha2']:
            code = keyval['currency']['code']
            symbol = keyval['currency']['symbol']
    f.close()
    return [code, symbol]



# api
def ajax(request):
    if request.is_ajax():
        user = request.user
        ser_instance = serializers.serialize('json', [ user ], fields=('email'))
        return JsonResponse({"user": ser_instance})

def home(request):
    return render(request, 'mainapp/home.html')

def about(request):
    return render(request, 'mainapp/about.html')

#api
def home_business_following(request):
    following = BusinessPost.objects.filter(business__followers=request.user)[:5]
    businesses = [{
        "name": business.business.name,
        "category": business.category.name,
        "content": business.content,
        "slug": business.get_absolute_url(),
    }for business in following]
    return JsonResponse(businesses, safe=False)


#api
def home_get_category(request, id):
    latitude = float(request.POST.get('latitude'))
    longitude = float(request.POST.get('latitude'))
    location = Point(longitude, latitude, srid=4326)
    category = get_object_or_404(BusinessCategory, id=id)
    businesses_qs = Business.objects.filter(category__id=id).annotate(distance=Distance(location, 'location')).order_by('distance')
    businesses = [{
        "name": business.name,
        "thumbnail": business.thumbnail.url,
        "category": business.category.name,
        "slug": business.get_absolute_url(),
        "rating": business.rating()["rating__avg"],
    }for business in businesses_qs]
    for b in businesses_qs:
        print(b.name, b.distance)
    context = {
        "category": category.name,
        "slug": category.slug,
        "businesses": businesses
    }
    return JsonResponse(context)


def all_business_category(request):
    categories = BusinessCategory.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'mainapp/all_business_category.html', context)

@login_required
def dashboard(request):
    user = request.user
    if 'page' in request.GET:
        page = request.GET.get('page')
        query_set = user.business_set.order_by('name')
        paginator = Paginator(query_set, 15)
        try:
            businesses = paginator.page(page)
        except EmptyPage:
            return JsonResponse("", safe=False)
        business_list = [{
            "name": business.name,
            "category": business.category.name,
            "followers": business.followers.count(),
            "url": business.get_absolute_url(),
            "image": business.thumbnail.url,
            "rating": business.rating()
        }for business in businesses]
        context = {
            "business": business_list,
            "has_next": businesses.has_next()
        }
        return JsonResponse(context)
    else:
        businesses = user.business_set.order_by('name')[:15]
        context = {
            'businesses': businesses,
            'web_root': settings.WEB_ROOT
        }
    return render(request, 'mainapp/dashboard.html', context)

def create_business(request):
    if not request.user.is_authenticated:
        return redirect(settings.CREATE_REDIRECT_URL)
    elif request.method == "POST":
        form = BusinessCreationForm(request.POST)
        if form.is_valid():
            new = form.save(commit=False)
            new.user = request.user
            new.save()
            notification = Notification.objects.create(
                content=f"Add a product to {new.name}",
                url=settings.WEB_ROOT+'/'+new.slug+'/add-product/',
                tag=new.name
            )
            notification.receivers.add(request.user)
            return HttpResponseRedirect(reverse('business-image', args=(new.slug,)))
        else:
            messages.error(request, "Something went wrong. Please try again.")
            return redirect('create-business')
    else:
        form = BusinessCreationForm()
    context = {
        'form': form
    }
    return render(request, 'mainapp/create_business.html', context)

@login_required
@business_owner_required
def business_thumbnail(request, slug):
    business = get_object_or_404(Business, slug=slug)
    if request.method == "POST":
        form = BusinessThumbnailForm(request.POST, request.FILES, instance=business)
        if form.is_valid():
            form.save()
        else:
            return JsonResponse({"error": form.errors}, status=400)
    else:
        form = BusinessThumbnailForm(instance=business)
    context = {
        'form': form,
        'business': business
    }
    return render(request, 'mainapp/business_thumbnail.html', context)


@login_required
@business_owner_required
def business_thumbnail2(request, slug):
    business = get_object_or_404(Business, slug=slug)
    form = BusinessThumbnailForm2(request.POST, request.FILES, instance=business)
    if form.is_valid():
        form.save()
        return JsonResponse("", status=200, safe=False)
    else:
        return JsonResponse({"error": form.errors}, status=400)



@login_required
@business_owner_required
@email_verify_required
def add_product(request, slug):
    business = get_object_or_404(Business, slug=slug)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            new = form.save(commit=False)
            new.business = business
            new.currency_code = currency(request)[0]
            new.currency = currency(request)[1]
            new.save()
            return JsonResponse(new.get_absolute_url(), safe=False)
        else:
            return JsonResponse({"error": form.errors}, status=400)
    else:
        form = ProductForm()
    context = {
        'form': form,
        'business': business,
        'currency': currency(request)[0]
    }
    return render(request, 'mainapp/add_products.html', context)



@login_required
@business_owner_required
@email_verify_required
def create_post(request, slug):
    business = get_object_or_404(Business, slug=slug)
    if request.method == "POST":
        form = CreateBusinessPost(request.POST)
        if form.is_valid():
            new = form.save(commit=False)
            new.business = business
            new.save()
            return HttpResponseRedirect(reverse('business-posts', args=(business.slug,)))
    else:
        form = CreateBusinessPost()
    context = {
        'form': form,
        'business': business
    }
    return render(request, 'mainapp/create_post.html', context)

def delete_post(request, id):
    if request.method == "POST":
        post = get_object_or_404(BusinessPost, id=id)
        if request.user == post.business.user:
            post.delete()
    return HttpResponseRedirect(reverse('business-detail', args=(post.business.slug,)))


def business_detail(request, slug):
    business = get_object_or_404(Business, slug=slug)
    business.business_visit(request, business)
    rated = business.rated(request)
    products = business.product_set.order_by('-date')[:3]
    context = {
        'business': business,
        'rated': rated,
        'products': products
    }
    return render(request, 'mainapp/business_detail.html', context)


def business_call(request):
    slug = request.POST.get('slug')
    business = get_object_or_404(Business, slug=slug)
    business.business_call(request, business)
    return JsonResponse("call", safe=False)


def business_direction(request, slug):
    business = get_object_or_404(Business, slug=slug)
    business.business_direction(request, business)
    return JsonResponse("direction", safe=False)

def business_insights(request, slug):
    business = get_object_or_404(Business, slug=slug)
    directions = business.business_directions()
    monthly_directions = business.monthly_business_directions()
    calls = business.business_calls()
    monthly_calls = business.monthly_business_calls()
    context = {
        "directions": directions,
        "monthly_directions": monthly_directions,
        "calls": calls,
        "monthly_calls": monthly_calls
    }
    return JsonResponse(context)


@business_owner_required
def delete_business(request, slug):
    return HttpResponseRedirect(reverse('delete-business-confirm', args=(slug,)))

@business_owner_required
def delete_business_confirm(request, slug):
    business = get_object_or_404(Business, slug=slug)
    if request.method == "POST":
        business.delete()
        return redirect('dashboard')
    else:
        context = {
            'business': business
        }
        return render(request, 'mainapp/delete_business_confirm.html', context)


'''def website_visit(request):
    url = request.GET['q']
    business = Business.objects.get(website=url)
    if request.user.is_authenticated:
        if WebsiteVisit.objects.filter(business=business, user=request.user).exists():
            pass
        else:
            WebsiteVisit.objects.create(business=business, user=request.user)
            notification = Notification.objects.create(
                    content=f'{request.user.name} just visited your website, {business.website}',
                    url=settings.WEB_ROOT+business.slug+'/'
                )
            notification.receivers.add(business.user)
    else:
        remote_addr = request.META.get('HTTP_X_FORWARDED_FOR')
        if remote_addr:
            address = remote_addr.split(',')[-1].strip()
        else:
            address = request.META.get('REMOTE_ADDR')
        if not IpUser.objects.filter(ip=address).exists():
            ipuser = IpUser.objects.create(ip=address)
            WebsiteVisit.objects.create(business=business, ipuser=ipuser)
            notification = Notification.objects.create(
                content=f'Someone just visited {business.name}',
                url=settings.WEB_ROOT+business.slug+'/'
            )
            notification.receivers.add(business.user) 
        else:
            ipuser = IpUser.objects.get(ip=address)
            if WebsiteVisit.objects.filter(business=business, ipuser=ipuser).exists():
                pass
            else:
                ipuser = IpUser.objects.get(ip=address)
                WebsiteVisit.objects.create(business=business, ipuser=ipuser)
                notification = Notification.objects.create(
                    content=f'Someone just visited {business.name}',
                    url=settings.WEB_ROOT+business.slug+'/'
                )
                notification.receivers.add(business.user) 
    print(url)
    return redirect(url)'''


@login_required
@business_owner_required
@email_verify_required
def edit_business(request, slug):
    business = get_object_or_404(Business, slug=slug)
    form = BusinessEditForm(request.POST or None, instance=business)
    contact_form = BusinessPersonalInfoEditForm(request.POST or None, instance=business)
    if form and contact_form.is_valid():
        form.save()
        contact_form.save()
        return HttpResponseRedirect(reverse('business-detail', args=(business.slug,)))
    context = {
        'business': business,
        'form': form,
        'contact_form': contact_form
    }
    return render(request, 'mainapp/business_edit.html', context)


# api
def business_home(request, slug):
    business = get_object_or_404(Business, slug=slug)
    last_post = business.businesspost_set.last()
    ratings = business.businessrating_set.order_by('-date_posted').exclude(content="")[:3]
    if last_post:
        post= {
            "business": {
                "name": last_post.business.name,
                "user": last_post.business.user.id
            },
            "category": last_post.category.name,
            "content": last_post.content[0:500],
            "date": naturalday(last_post.date),
            "post": last_post.id,
            "likes": last_post.likes.count(),
            "liked": last_post.liked(request.user.id)
        }
    else:
        post = {}
    ratings_list = [{
        "rating": rating.rating,
        "content": rating.content,
        "date_posted": naturalday(rating.date_posted),
        "user": {
            "id": rating.user.id,
            "name": rating.user.name
        },
        "image": rating.user.image.url,
        "review": rating.id
    }for rating in ratings]
    return JsonResponse({"post": post, "ratings": ratings_list})


# api
def business_products(request, slug):
    business = get_object_or_404(Business, slug=slug)
    if 'page' in request.GET:    
        page = request.GET.get('page')
        query_set = business.product_set.order_by('-date')
        paginator = Paginator(query_set, 15)
        try:
            products = paginator.page(page)
        except EmptyPage:
            return JsonResponse("", safe=False)
        products_list = [{
            "id": product.id,
            "slug": product.slug,
            "name": product.name,       
            "description": product.description,
            "currency": product.currency,
            "price": product.price,
            "image": product.image.url,
            "rating": product.rating()
        }for product in products]
        context = {
            "products": products_list,
            "has_next": products.has_next()
        }
        return JsonResponse(context)
    else:
        products = business.product_set.order_by('-date')[:15]
        context = {
            'business': business,
            'products': products
        }
        return render(request, 'mainapp/business_products.html', context)


# api
def business_posts(request, slug):
    business = get_object_or_404(Business, slug=slug)
    if 'page' in request.GET:
        page = request.GET.get('page')
        query_set = business.businesspost_set.order_by('-date')
        paginator = Paginator(query_set, 5)
        try:
            posts = paginator.page(page)
        except EmptyPage:
            return JsonResponse("", safe=False)
        posts_list = [{
            "id": post.id,
            "business": {
                "name": post.business.name,
                "slug": post.business.slug,
                "user": post.business.user.id
            },
            "category": {
                "name": post.category.name,
                "slug": post.category.slug
            },
            "content": post.content,
            "date": naturalday(post.date),
            "post": post.id,
            "likes": post.likes.count(),
            "liked": post.liked(request.user.id)
        }for post in posts]
        context = {
            "posts": posts_list,
            "has_next": posts.has_next()
        }
        return JsonResponse(context)
    else:
        posts = business.businesspost_set.order_by('-date')[:5]
        business_posts = [{
            "id": post.id,
            "business": {
                "name": post.business.name,
                "slug": post.business.slug,
                "user": post.business.user
            },
            "category": {
                "name": post.category.name,
                "slug": post.category.slug
            },
            "content": post.content,
            "date": naturalday(post.date),
            "post": post.id,
            "likes": post.likes.count(),
            "liked": post.liked(request.user.id)
        }for post in posts]
        context = {
            "posts": business_posts,
            "business": business
        }
        return render(request, 'mainapp/business_posts.html', context)


#api
def follow(request, business_id):
    if request.is_ajax and request.method == "POST":
        business = get_object_or_404(Business, id=business_id)
        if business.followers.filter(id=request.user.id).exists():
            business.followers.remove(request.user)
            return JsonResponse("unfollowed", safe=False)
        else:
            business.followers.add(request.user)
            if business.user != request.user:
                notification = Notification.objects.create(
                    content=f'{request.user.name} just followed {business.name}',
                    url=settings.WEB_ROOT+'/'+business.slug+'/',
                    tag=business.name
                )
                notification.receivers.add(business.user) 
            return JsonResponse("followed", safe=False)

def followers(request, slug):
    business = get_object_or_404(Business, slug=slug)
    if 'page' in request.GET:
        page = request.GET.get('page')
        query_set = business.followers.order_by('name')
        paginator = Paginator(query_set, 20)
        try:
            followers = paginator.page(page)
        except EmptyPage:
            return JsonResponse("", safe=False)
        followers_list = [{
            "name": follower.name,
            "slug": follower.slug,
            "image": follower.image.url
        }for follower in followers]
        context = {
            "followers": followers_list,
            "has_next": followers.has_next()
        }
        return JsonResponse(context)
    else:
        followers = business.followers.order_by('name')[:20]
        context = {
            'business': business,
            'followers': followers,
            'web_root': settings.WEB_ROOT
        }
    return render(request, 'mainapp/followers.html', context)


def business_post_detail(request, slug, post_id):
    post = get_object_or_404(BusinessPost, id=post_id, business__slug=slug)
    if 'page' in request.GET:
        page = request.GET.get('page')
        query_set = post.businesspostcomment_set.order_by('-datetime')
        paginator = Paginator(query_set, 10)
        try:
            comments = paginator.page(page)
        except EmptyPage:
            return JsonResponse("", safe=False)
        comments_list = [{
            "id": comment.id,
            "content": comment.content,
            "date": naturalday(comment.datetime),
            "post":{
                "user": comment.post.business.user.id
            },
            "user": {
                "id": comment.author.id,
                "name": comment.author.name,
                "image": comment.author.image.url
            }
        }for comment in comments]
        context = {
            "comments": comments_list,
            "has_next": comments.has_next()
        }
        return JsonResponse(context)
    else:
        comments = post.businesspostcomment_set.order_by('-datetime')[:10]
        form = BusinessPostCommentForm(request.POST or None)
        if form.is_valid():
            new = form.save(commit=False)
            new.author = request.user
            new.post = post
            new.save()
            return HttpResponseRedirect(reverse('business-post-detail', args=(slug, post.id,)))
        post_dict = {
            'date': post.date,
            'content': post.content,
            'id': post.id,
            'business': {
                'slug': post.business.slug,
                'name': post.business.name,
                "user": post.business.user
            },
            'liked': post.liked(request.user.id)
        }       
        context = {
            'post': post_dict,
            'comments': comments,
            'form': form
        }
        return render(request, 'mainapp/business_post.html', context)


def delete_comment(request, id):
    if request.method == "POST":
        comment = get_object_or_404(BusinessPostComment, id=id)
        if comment.author == request.user:
            comment.delete()
    return HttpResponseRedirect(reverse('business-post-detail', args=(comment.post.business.slug, comment.post.id,)))


def like_post(request):
    if request.is_ajax and request.method == "POST":
        post_id = request.POST.get('post')
        post = get_object_or_404(BusinessPost, id=post_id)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            return JsonResponse("unliked", safe=False)
        else:
            post.likes.add(request.user)
            if post.business.user != request.user:
                notification = Notification.objects.create(
                    content=f'{request.user.name} just liked your post',
                    url=settings.WEB_ROOT+'/'+post.business.slug+'/post/'+str(post.id)+'/',
                    tag=post.business.name
                )
                notification.receivers.add(post.business.user)
            return JsonResponse("liked", safe=False)


def business_category(request, slug):
    page = request.GET.get('page')
    if 'lon' and 'lat' in request.GET:
        str_longitude = request.GET['lon']
        str_latitude = request.GET['lat']    
        longitude = float(str_longitude)
        latitude = float(str_latitude)
    else:
        from django.contrib.gis.geoip2 import GeoIP2
        g = GeoIP2()
        remote_addr = request.META.get('HTTP_X_FORWARDED_FOR')
        if remote_addr:
            address = remote_addr.split(',')[-1].strip()
        else:
            address = request.META.get('REMOTE_ADDR')
        if settings.DEBUG == True:
            latitude = g.lat_lon(settings.DEV_GEOLOCATION_IP)[0]
            longitude = g.lat_lon(settings.DEV_GEOLOCATION_IP)[1]
        else:
            latitude = g.lat_lon(address)[0]
            longitude = g.lat_lon(address)[1]
    location = Point(longitude, latitude, srid=4326)
    category = get_object_or_404(BusinessCategory, slug=slug)
    businesses = category.business_set.annotate(distance=Distance(location, 'location')).order_by('distance')
    paginator = Paginator(businesses, 25)
    try:
        paginated_businesses = paginator.page(page)
    except PageNotAnInteger:
        paginated_businesses = paginator.page(1)
    except EmptyPage:
        paginated_businesses = paginator.page(paginator.num_pages)
    context = {
        'category': category,
        'businesses': paginated_businesses
    }
    return render(request, 'mainapp/business_category.html', context)


def edit_product(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if product.business.user == request.user:
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES, instance=product)
            if form.is_valid():
                new = form.save(commit=False)
                new.save()
                return JsonResponse(new.get_absolute_url(), safe=False)
            else:
                return JsonResponse({"error": form.errors}, status=400)
        else:
            form = ProductForm(instance=product)
        context = {
            'form': form,
            'product': product
        }
    else:
        return HttpResponseRedirect(reverse('product-detail', args=(product.slug,)))
    return render(request, 'mainapp/edit_product.html', context)


def delete_product(request, slug):
    return HttpResponseRedirect(reverse('delete-product-confirm', args=(slug,)))

def delete_product_confirm(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.method == "POST":
        if request.user == product.business.user:
            product.delete()
            return HttpResponseRedirect(reverse('business-detail', args=(product.business.slug,)))
    else:
        context = {
            'product': product
        }
        return render(request, 'mainapp/delete_product_confirm.html', context)


def business_product(request, slug):
    business = get_object_or_404(Business, slug=slug)
    products = business.product_set.order_by('-date')
    context = {
        'business': business,
        'products': products
    }
    return render(request, 'mainapp/business_products.html', context)


def product_detail(request, business, slug):
    product = get_object_or_404(Product, slug=slug)
    rated = product.rated(request)
    saved = product.saved(request)
    context = {
        'product': product,
        'rated': rated,
        'saved': saved
    }
    return render(request, 'mainapp/product_detail.html', context)


def related_products(request):
    slug = request.GET['q']
    from django.contrib.gis.geoip2 import GeoIP2
    g = GeoIP2()
    remote_addr = request.META.get('HTTP_X_FORWARDED_FOR')
    if remote_addr:
        address = remote_addr.split(',')[-1].strip()
    else:
        address = request.META.get('REMOTE_ADDR')
    if settings.DEBUG == True:
        latitude = g.lat_lon(settings.DEV_GEOLOCATION_IP)[0]
        longitude = g.lat_lon(settings.DEV_GEOLOCATION_IP)[1]
    else:
        latitude = g.lat_lon(address)[0]
        longitude = g.lat_lon(address)[1]
    location = Point(longitude, latitude, srid=4326)
    if slug:
        product = Product.objects.get(slug=slug)
        query = SearchQuery(product.name)
        products_vector = SearchVector('name', weight='A') + SearchVector('category__name', config='english', weight='B') + SearchVector('description', config='english', weight='C')
        products_query_set = Product.objects.annotate(search=products_vector, rank=SearchRank(products_vector, query)).filter(search=query).exclude(id=product.id).order_by('-rank')
        products = products_query_set.annotate(distance=Distance(location, 'business__location')).order_by('distance')
        if not products:
            return JsonResponse("", safe=False)
        products_list = [{
            "name": product.name,
            "image": product.image.url,
            "currency": product.currency,
            "price": product.price,
            "rating": product.rating(),
            "url": product.get_absolute_url()
        }for product in products]
        return JsonResponse(products_list, safe=False)


def search(request):
    search_term = request.GET['q']
    search_type = request.GET.get('type')
    page = request.GET.get('page')
    if 'lon' and 'lat' in request.GET:
        str_longitude = request.GET['lon']
        str_latitude = request.GET['lat']    
        longitude = float(str_longitude)
        latitude = float(str_latitude)
    else:
        from django.contrib.gis.geoip2 import GeoIP2
        g = GeoIP2()
        remote_addr = request.META.get('HTTP_X_FORWARDED_FOR')
        if remote_addr:
            address = remote_addr.split(',')[-1].strip()
        else:
            address = request.META.get('REMOTE_ADDR')
        if settings.DEBUG == True:
            latitude = g.lat_lon(settings.DEV_GEOLOCATION_IP)[0]
            longitude = g.lat_lon(settings.DEV_GEOLOCATION_IP)[1]
        else:
            latitude = g.lat_lon(address)[0]
            longitude = g.lat_lon(address)[1]
    location = Point(longitude, latitude, srid=4326)
    if search_term:
        query = SearchQuery(search_term)
        if search_type == "products":
            vector = SearchVector('name', weight='A') + SearchVector('description', config='english', weight='B')
            query_set = Product.objects.annotate(search=vector, rank=SearchRank(vector, query)).filter(search=query).order_by('-rank')
            products = query_set.annotate(distance=Distance(location, 'business__location')).order_by('distance')
            paginator = Paginator(products, 30)
            try:
                paginated = paginator.page(page)
            except PageNotAnInteger:
                paginated = paginator.page(1)
            except EmptyPage:
                paginated = paginator.page(paginator.num_pages)
            context = {
                'products': paginated,
                'search_term': search_term,
                'search_type': search_type
            }
        else:
            business_vector = SearchVector('name', weight='A') + SearchVector('category__name', weight='B') + SearchVector('description', config='english', weight='C')
            business_query_set = Business.objects.annotate(search=business_vector, rank=SearchRank(business_vector, query)).filter(search=query).order_by('-rank')            
            businesses = business_query_set.annotate(distance=Distance(location, 'location')).order_by('distance')
            paginator = Paginator(businesses, 30)
            try:
                paginated = paginator.page(page)
            except PageNotAnInteger:
                paginated = paginator.page(1)
            except EmptyPage:
                paginated = paginator.page(paginator.num_pages)
            context = {
                'businesses': paginated,
                'search_term': search_term,
                'search_type': search_type
            }
        return render(request, 'mainapp/search.html', context)


def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)

def service_worker(request):
    sw_path = settings.BASE_DIR / "static/js" / "service_worker.js"
    response = HttpResponse(open(sw_path).read(), content_type='application/javascript')
    return response

def webmanifest(request):
    sw_path = settings.BASE_DIR / "static/json" / "manifest.webmanifest"
    response = HttpResponse(open(sw_path).read(), content_type='application/javascript')
    return response