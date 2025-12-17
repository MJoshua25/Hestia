from .models import Notification
from django.contrib.auth import get_user_model

User = get_user_model()

class NotificationService:
    @staticmethod
    def create_notification(user, type, title, message, link=''):
        """
        Create a notification for a specific user.
        """
        if not user:
            return None
            
        return Notification.objects.create(
            user=user,
            type=type,
            title=title,
            message=message,
            link=link
        )

    @staticmethod
    def create_bulk_notifications(users, type, title, message, link=''):
        """
        Create the same notification for multiple users efficiently.
        """
        notifications = [
            Notification(
                user=user,
                type=type,
                title=title,
                message=message,
                link=link
            ) for user in users if user
        ]
        
        return Notification.objects.bulk_create(notifications)
