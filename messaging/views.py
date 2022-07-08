from django.conf import settings
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from users.decorators import email_verify_required
from django.http.response import JsonResponse, HttpResponse
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from .models import User, Message, Chat
from mainapp.models import Business
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.humanize.templatetags.humanize import naturaltime, naturalday
# Create your views here.

def template(request):
    return render(request, 'messaging/template.html')

@login_required
@email_verify_required
def messages(request):
    user = request.user
    if 'page' in request.GET:
        page = request.GET.get('page')
        query_set = Chat.objects.filter(Q(receiver=user) | Q(sender=user))
        paginator = Paginator(query_set, 15)
        try:
            chats = paginator.page(page)
        except EmptyPage:
            return JsonResponse("", safe=False)
        chats_list = [{
            'sender': chat.sender.slug,
            'receiver': chat.receiver.slug,
            'sender_name': chat.sender.name,
            'receiver_name': chat.receiver.name,
            'sender_image': chat.sender.image.url,
            'receiver_image': chat.receiver.image.url,
            'last_message': chat.last_message().message,
            'last_message_sender': chat.last_message().sender.slug,
            'last_message_timestamp': naturalday(chat.last_message().timestamp),
            'last_message_seen': chat.last_message_seen()
        }for chat in chats]
        context = {
            'chats': chats_list,
            'has_next': chats.has_next()
        }
        return JsonResponse(context)
    else:
        chats = Chat.objects.filter(Q(receiver=user) | Q(sender=user))[:15]
        context = {
            'chats': chats,
            'web_root': settings.WEB_ROOT
        }
    return render(request, 'messaging/messages.html', context)



@login_required
@email_verify_required
def load_messages(request, slug):
    other_user = get_object_or_404(User, slug=slug)
    if other_user == request.user:
        return redirect('messages')
    messages = Message.objects.filter(
        receiver=request.user, sender=other_user
    )
    messages.update(seen=True)
    messages = messages | Message.objects.filter(receiver=other_user, sender=request.user).order_by('timestamp')
    seen = ""
    if messages:
        last_message = messages.last()
        if last_message.sender == request.user:
            if last_message.seen == True:
                seen = "seen"
            else:
                seen = "sent"
    other_user = {
        "name": other_user.name,
        "slug": other_user.slug,
        "image": other_user.image.url
    }
    messages = [{
        "message": message.message,
        "sent": message.sender == request.user,
        "timestamp": naturaltime(message.timestamp),
        "sender": message.sender.name
    }for message in messages]
    context = {
        "other_user": other_user,
        "messages": messages[-10:],
        "seen": seen,
        "web_root": settings.WEB_ROOT
    }
    if request.is_ajax():
        return JsonResponse(context)
    else:
        return render(request, 'messaging/message_box.html', context)

def ajax_load_messages(request, slug):
    other_user = get_object_or_404(User, slug=slug)
    messages = Message.objects.filter(seen=False).filter(
        receiver=request.user, sender=other_user
    )   
    message_list = [{
        "message": message.message,
        "timestamp": naturaltime(message.timestamp),
        "sent": message.sender == request.user,
    }for message in messages]
    messages.update(seen=True)
    if request.method == "POST":
        try:
            chat = Chat.objects.get(Q(receiver=request.user, sender=other_user) | Q(receiver=other_user, sender=request.user))
        except ObjectDoesNotExist:
            chat = Chat.objects.create(sender=request.user, receiver=other_user)
        message = request.POST.get('message')
        new = Message.objects.create(
            chat=chat,
            receiver=other_user,
            sender=request.user,
            message=message
        )
        message_list.append({
            "message": new.message,
            "timestamp": naturaltime(new.timestamp),
            "sent": True,
        })
        print(message_list)
    return JsonResponse(message_list, safe=False)


def previous_messages(request, slug):
    other_user = get_object_or_404(User, slug=slug)
    messages = Message.objects.filter(
        Q(receiver=request.user, sender=other_user) | Q(receiver=other_user, sender=request.user)
    ).order_by('-timestamp')
    paginator = Paginator(messages, 20)
    page = request.GET.get('page')
    try:
        paginated_messages = paginator.page(page)
    except PageNotAnInteger:
        return JsonResponse({"messages": "An error occured"})  
    except EmptyPage:
        return JsonResponse({"messages": "No more messages"})
    messages_list = [{
        "message": message.message,
        "sent": message.sender == request.user,
        "timestamp": naturaltime(message.timestamp),
        "sender": message.sender.name
    }for message in paginated_messages]
    context = {
        "messages": messages_list,
        "has_next": paginated_messages.has_next(),
    }
    return JsonResponse(context)


def message_count(request):
    messages = Message.objects.filter(receiver=request.user, seen=False).count()
    if messages == 0:
        return JsonResponse("", safe=False)
    elif messages > 9:
        return JsonResponse("9+", safe=False)
    else:
        return JsonResponse(messages, safe=False)