from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
import requests
from django.conf import settings


@receiver(post_save, sender=User)
def send_welcome_notification(sender, instance, created, *args, **kwargs):
    if created:
        try:
            url = "http://novu.duvindu.org/api/v1/events/trigger"
            headers = {
                "Authorization": f"ApiKey {settings.NOVU_API_KEY}",
                "Content-Type": "application/json",
                "Connection": "close",
            }
            payload = {
                "name": "welcome-email",
                "to": {
                    "subscriberId": str(instance.id),
                    "email": instance.email,
                },
                "payload": {
                    "username": instance.username,
                },
            }

            response = requests.post(url, json=payload, headers=headers)

        except Exception as e:
            print("NOVU ERROR:", str(e))