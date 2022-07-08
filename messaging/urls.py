from django.urls import path
from . import views

urlpatterns = [
    path('template/', views.template),
    #path('send-message/<str:user_slug>-<user_id>/', views.send_message, name='send-message'),
    path('messages/', views.messages, name='messages'),
    path('messages/<slug:slug>/', views.load_messages, name='load-message'),
    path('ajax/message/<slug:slug>/', views.ajax_load_messages, name='ajax-load-messages'),
    path('previous-messages/<slug:slug>/', views.previous_messages, name='previous-messages'),
    path('message-count/', views.message_count, name='message-count'),
]