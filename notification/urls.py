from django.urls import path
from . import views

urlpatterns = [
    path('ajax-notification/', views.ajax_notification, name='ajax-notification'),
    path('notifications/', views.notifications, name='notifications'),
    path('notification/<int:notification_id>/', views.notification, name='notification'),
    path('notification-count/', views.notification_count, name='notification-count')
]