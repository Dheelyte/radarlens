from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.http.response import JsonResponse
from django.shortcuts import redirect, render, reverse, get_object_or_404
from rating.models import BusinessRating, ProductRating
from .models import ReportBusiness, ReportBusinessComment, ReportBusinessReview, ReportBusinessPost, ReportProduct, ReportProductReview
from .forms import ContactForm
from mainapp.models import Business, BusinessPost, Product, BusinessPostComment
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist

def report_business(request, slug):
    if request.user.email_is_verified != True:
        return JsonResponse("You need to verify your email")
    business = get_object_or_404(Business, slug=slug)
    if business.user != request.user:
        if business.reportbusiness_set.filter(user=request.user).exists():
            return JsonResponse('You have reported this business', safe=False)
        else:
            ReportBusiness.objects.create(business=business, user=request.user)
            email = settings.FEEDBACK_EMAIL
            subject = "Report Business"
            message = render_to_string('feedback/report_business_email.html', {
                'subject': subject,
                'business': business,
                'user': request.user
            })
            email = EmailMessage(
                subject, message, to=[email]
            )
            email.content_subtype = 'html'
            email.send(fail_silently=False)
            return JsonResponse('You have reported this business', safe=False)

def report_product(request, slug):
    if request.user.email_is_verified != True:
        return JsonResponse("You need to verify your email")
    product = get_object_or_404(Product, slug=slug)
    if product.business.user != request.user:
        if product.reportproduct_set.filter(user=request.user).exists():
            return JsonResponse('You have reported this product', safe=False)
        else:
            ReportProduct.objects.create(product=product, user=request.user)
            email = settings.FEEDBACK_EMAIL
            subject = "Report Product"
            message = render_to_string('feedback/report_product_email.html', {
                'subject': subject,
                'product': product,
                'user': request.user
            })
            email = EmailMessage(
                subject, message, to=[email]
            )
            email.content_subtype = 'html'
            email.send(fail_silently=False)
            return JsonResponse('You have reported this product', safe=False)

def report_post(request):
    if request.user.email_is_verified != True:
        return JsonResponse("You need to verify your email")
    post_id = request.POST.get('post')
    post = get_object_or_404(BusinessPost, id=post_id)
    if post.business.user != request.user:
        if post.reportbusinesspost_set.filter(user=request.user).exists():
            return JsonResponse("You have reported this post", safe=False)
        else:
            ReportBusinessPost.objects.create(post=post, user=request.user)
            email = settings.FEEDBACK_EMAIL
            subject = "Report Post"
            message = render_to_string('feedback/report_post_email.html', {
                'subject': subject,
                'post': post,
                'user': request.user
            })
            email = EmailMessage(
                subject, message, to=[email]
            )
            email.content_subtype = 'html'
            email.send()
            return JsonResponse("You have reported this post", safe=False)


def report_review(request):
    if request.user.email_is_verified != True:
        return JsonResponse("You need to verify your email")
    review_id = request.POST.get('review')
    review = get_object_or_404(BusinessRating, id=review_id)
    if review.user != request.user:
        if review.reportbusinessreview_set.filter(user=request.user).exists():
            return JsonResponse("You have reported this review", safe=False)
        else:
            ReportBusinessReview.objects.create(review=review, user=request.user)
            email = settings.FEEDBACK_EMAIL
            subject = "Report Business Review"
            message = render_to_string('feedback/report_business_review_email.html', {
                'subject': subject,
                'review': review,
                'user': request.user
            })
            email = EmailMessage(
                subject, message, to=[email]
            )
            email.content_subtype = 'html'
            email.send(fail_silently=False)
            return JsonResponse("You have reported this review.", safe=False)


def report_product_review(request):
    if request.user.email_is_verified != True:
        return JsonResponse("You need to verify your email")
    review_id = request.POST.get('review')
    review = get_object_or_404(ProductRating, id=review_id)
    if review.user != request.user:
        if review.reportproductreview_set.filter(user=request.user).exists():
            return JsonResponse("You have reported this review", safe=False)
        else:
            ReportProductReview.objects.create(review=review, user=request.user)
            email = settings.FEEDBACK_EMAIL
            subject = "Report Product Review"
            message = render_to_string('feedback/report_product_review_email.html', {
                'subject': subject,
                'review': review,
                'user': request.user
            })
            email = EmailMessage(
                subject, message, to=[email]
            )
            email.content_subtype = 'html'
            email.send(fail_silently=False)
            return JsonResponse("You have reported this review.", safe=False)


def report_comment(request):
    if request.user.email_is_verified != True:
        return JsonResponse("You need to verify your email")
    comment_id = request.POST.get('comment')
    comment = get_object_or_404(BusinessPostComment, id=comment_id)
    if comment.author != request.user:
        if comment.reportbusinesscomment_set.filter(user=request.user).exists():
            return JsonResponse("You have reported this comment", safe=False)
        else:
            ReportBusinessComment.objects.create(comment=comment, user=request.user)
            email = settings.FEEDBACK_EMAIL
            subject = "Report Comment"
            message = render_to_string('feedback/report_comment_email.html', {
                'subject': subject,
                'comment': comment,
                'user': request.user
            })
            email = EmailMessage(
                subject, message, to=[email]
            )
            email.content_subtype = 'html'
            email.send()
            return JsonResponse("You have reported this comment.", safe=False)

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            new = form.save(commit=False)
            new.user = request.user
            new.save()
            email = settings.FEEDBACK_EMAIL
            subject = form.cleaned_data['subject']
            message = render_to_string('feedback/contact_email.html', {
                'subject': subject,
                'content': form.cleaned_data['content'],
                'user': request.user
            })
            email = EmailMessage(
                subject, message, to=[email]
            )
            email.content_subtype = 'html'
            email.send()
            messages.success(request, 'We have received your message. We will get back to you shortly.')
            return redirect('contact')
    else:
        form = ContactForm()
    context = {
        'form': form
    }
    return render(request, 'feedback/contact.html', context)