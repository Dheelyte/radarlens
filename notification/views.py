from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from.models import Notification
from users.decorators import email_verify_required
from django.core.paginator import Paginator, EmptyPage
from django.http import JsonResponse, HttpResponseRedirect
from django.core import serializers
from django.contrib.humanize.templatetags.humanize import naturaltime


def notification(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    url = notification.url
    notification.seen = True
    notification.save()
    return redirect(url)


@email_verify_required
def notifications(request):
    if 'page' in request.GET:
        page = request.GET.get('page')
        query_set = Notification.objects.filter(receivers=request.user).order_by('-time')
        paginator = Paginator(query_set, 20)
        try:
            notifications = paginator.page(page)
        except EmptyPage:
            return JsonResponse("", safe=False)
        notification_list = [{
            "id": notification.id,
            "content": notification.content,
            "time": naturaltime(notification.time),
            "tag": notification.tag,
            "seen": notification.seen
        }for notification in notifications]
        context = {
            "notifications": notification_list,
            "has_next": notifications.has_next()
        }
        return JsonResponse(context)
    else:
        notifications = Notification.objects.filter(receivers=request.user).order_by('-time')[:20]
        not_seen = Notification.objects.filter(receivers=request.user, lazy_seen=False)
        not_seen.update(lazy_seen=True)
        context = {
            'notifications': notifications,
            'web_root': settings.WEB_ROOT
        }
    return render(request, 'notification/notifications.html', context)


def ajax_notification(request):
    if request.is_ajax():
        notifications_qs = Notification.objects.filter(receivers=request.user).order_by('-time')[:5]
        notifications = [{
            "id": notification.pk,
            "content": notification.content,
            "url": notification.url,
            "seen": notification.seen,
            "time": naturaltime(notification.time),
            "tag": notification.tag
        }for notification in notifications_qs]
        not_seen = Notification.objects.filter(receivers=request.user, lazy_seen=False)
        not_seen.update(lazy_seen=True)
        return JsonResponse({"notifications": notifications})

def notification_count(request):
    count = Notification.objects.filter(receivers=request.user, lazy_seen=False).count()
    if count == 0:
        return JsonResponse("", safe=False)
    elif count > 9:
        return JsonResponse("9+", safe=False)
    else:
        return JsonResponse(count, safe=False)

    