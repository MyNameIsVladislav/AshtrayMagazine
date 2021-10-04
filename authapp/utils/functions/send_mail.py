from django.core.mail import send_mail
from django.urls import reverse
from django.utils.safestring import mark_safe

from core import settings


def send_verify_mail(user):
    verify_link = reverse(
        'auth:verify',
        args=[user.email, user.activation_key])
    key_activation = mark_safe(f'<a href="{settings.DOMAIN_NAME}{verify_link}"> Активировать </a>')
    title = 'Подтверждение учетной записи'
    message = f'Для подтверждения учетной записи {user.email}' \
              f' пройдите по ссылке: {key_activation}'

    return send_mail(
        title,
        message,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
        html_message=message
    )
