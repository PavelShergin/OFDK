import uuid
from datetime import timedelta
from celery import shared_task
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from users.models import User, EmailVerification
from django.core.mail import EmailMessage
from django.urls import reverse
from django.conf import settings


@shared_task
def send_email_verification(user_id):
    try:
        user = User.objects.get(id=user_id)
    except ObjectDoesNotExist:
        # Обработка ошибки, если пользователь не найден
        return "User not found"

    expiration = timezone.now() + timedelta(hours=48)

    try:
        record = EmailVerification.objects.create(code=uuid.uuid4(), user=user, expiration=expiration)
    except Exception as e:
        # Обработка ошибки при создании записи EmailVerification
        return f"Error creating EmailVerification: {e}"

    try:
        record.send_verification_email()
    except Exception as e:
        # Обработка ошибки при отправке письма верификации
        return f"Error sending verification email: {e}"
