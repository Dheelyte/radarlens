from django.conf import settings
from django.shortcuts import render, reverse, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from mainapp.models import Business, Product
from .models import BusinessRating, ProductRating
from .forms import BusinessRatingForm, ProductRatingForm
from notification.models import Notification
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage
from django.contrib.humanize.templatetags.humanize import naturalday

# api
def business_reviews(request, slug):
    business = get_object_or_404(Business, slug=slug)
    if 'page' in request.GET:
        page = request.GET.get('page')
        query_set = business.businessrating_set.exclude(content="").order_by('-date_posted')
        paginator = Paginator(query_set, 10)
        try:
            reviews = paginator.page(page)
        except EmptyPage:
            return JsonResponse("", safe=False)
        reviews_list = [{
            "id": review.id,
            "rating": review.rating,
            "content": review.content,
            "date": naturalday(review.date_posted),
            "user": {
                "name": review.user.name,
                "id": review.user.id,
                "image": review.user.image.url
            }
        }for review in reviews]
        context = {
            "reviews": reviews_list,
            "has_next": reviews.has_next()
        }
        return JsonResponse(context)
    else:
        ratings = business.businessrating_set.exclude(content="").order_by('-date_posted')[:10]
        rated = business.rated(request)
        context = {
            'business': business,
            'ratings': ratings,
            'rated': rated
        }
        return render(request, 'rating/business_reviews.html', context)



def business_rating(request, slug):
    business = get_object_or_404(Business, slug=slug)
    if request.is_ajax and request.method == "POST" and request.user != business.user:
        try:
            business.businessrating_set.get(user=request.user)
            form = BusinessRatingForm(request.POST, instance=business)
        except:
            form = BusinessRatingForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.business = business
            instance.user = request.user
            instance.save()
            notification = Notification.objects.create(
                content=f"{request.user.name} wrote a review on {business.name}",
                url=settings.WEB_ROOT+business.get_absolute_url(),
                tag = business.name
            )
            notification.receivers.add(business.user)
            return JsonResponse("Rating successful", safe=False)
        else:
            return JsonResponse("Something went wrong", status=400, safe=False)



def edit_business_rating(request, slug):
    business = get_object_or_404(Business, slug=slug)
    if request.user == business.user:
        return HttpResponseRedirect(reverse('business-detail', args=(business.slug,)))
    try:
        review = business.businessrating_set.get(user=request.user)
        form = BusinessRatingForm(request.POST or None, instance=review)
    except ObjectDoesNotExist:
        form = BusinessRatingForm(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('business-detail', args=(business.slug,)))
    context = {
        'business': business,
        'form': form
    }
    return render(request, 'rating/edit_business_rating.html', context)

def product_rating(request, slug):
    product = get_object_or_404(Product, slug=slug)
    ratings = product.productrating_set.all().order_by('-date_posted')
    if request.is_ajax and request.method == "POST":
        form = ProductRatingForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.product = product
            instance.user = request.user
            instance.save()
            return JsonResponse("success", safe=False, status=200)
        else:
            return JsonResponse({"error": form.errors}, status=400)


def product_reviews(request, slug):
    page = request.GET.get('page')
    product = get_object_or_404(Product, slug=slug)
    query_set = product.productrating_set.order_by('-date_posted')
    paginator = Paginator(query_set, 10)
    try:
        reviews = paginator.page(page)
    except EmptyPage:
        return JsonResponse("", safe=False)
    reviews_list = [{
        "id": review.id,
        "rating": review.rating,
        "content": review.content,
        "date": naturalday(review.date_posted),
        "user": {
            "id": review.user.id,
            "name": review.user.name,
            "image": review.user.image.url
        }
    }for review in reviews]
    context = {
        "reviews": reviews_list,
        "has_next": reviews.has_next()
    }
    return JsonResponse(context)


def delete_business_review(request, id):
    if request.method == "POST":
        review = get_object_or_404(BusinessRating, id=id)
        if review.user == request.user:
            review.delete()
    return HttpResponseRedirect(reverse('business-detail', args=(review.business.slug,)))


def delete_product_review(request, id):
    if request.method == "POST":
        review = get_object_or_404(ProductRating, id=id)
        if review.user == request.user:
            review.delete()
    return HttpResponseRedirect(reverse('product-detail', args=(review.product.slug,)))