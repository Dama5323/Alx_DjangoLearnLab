from django.urls import path
from .views import NotificationListView, UnreadNotificationCountView

urlpatterns = [
    path('', NotificationListView.as_view(), name='notification-list'),
    path('unread-count/', UnreadNotificationCountView.as_view(), name='unread-notification-count'),
]