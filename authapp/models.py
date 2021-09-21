from datetime import timedelta
<<<<<<< HEAD
=======
import re
>>>>>>> CN-26

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext as _
from django.db.models.signals import post_save
from django.dispatch import receiver
<<<<<<< HEAD
from django.core.validators import RegexValidator
=======
from django.core.validators import BaseValidator
>>>>>>> CN-26
from django.utils.timezone import now

from authapp.managers import CustomUserManager


<<<<<<< HEAD
# Create your models here.

=======
>>>>>>> CN-26
class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    birthday = models.DateField(_('birthday'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

<<<<<<< HEAD
=======
    # для отправки почты при регистрации
>>>>>>> CN-26
    activation_key = models.CharField(
        max_length=128,
        blank=True
    )
    activation_key_expires = models.DateTimeField(
        default=(now() + timedelta(hours=48))
    )

    def is_activation_key_expired(self):
        if now() <= self.activation_key_expires:
            return False
        else:
            return True

    def __str__(self):
        return self.email


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'users_avatar/user_{0}/{1}'.format(instance.user.id, filename)


class RegexValidatorPhone(BaseValidator):
    message = 'Некорректный номер телефона'

    def compare(self, phone, valid_phone):
        return not re.match(valid_phone, phone)


class UserProfile(models.Model):
    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')

    MALE = 'M'
    FEMALE = 'W'

    RU = 'RU'
    EN = 'EN'

    GENDER_CHOICES = (
        (MALE, _('MAN')),
        (FEMALE, _('WOMAN')),
    )
    REGION_CHOICE = (
        (RU, 'RU'),
        (EN, 'EN'),
    )
<<<<<<< HEAD
    phone_validator = RegexValidator(regex=r'^\+&7|1?\d{8,15}$')
=======
    phone_validator = RegexValidatorPhone(limit_value=r'^(\+(7|1)|8)[0-9]{9}')
>>>>>>> CN-26

    user = models.OneToOneField(User, unique=True, null=False,
                                db_index=True, on_delete=models.CASCADE)
    gender = models.CharField(verbose_name=_('gender'), max_length=10, choices=GENDER_CHOICES, blank=True)
    avatar = models.ImageField(verbose_name=_('avatar'), upload_to=user_directory_path, default='default/default.jpg')
    region = models.CharField(verbose_name=_('region'), max_length=2, choices=REGION_CHOICE)
    phone = models.CharField(verbose_name=_('phone'), validators=[phone_validator],
                             max_length=16, blank=True, help_text='+7..........')

    def __str__(self):
        return f'Профиль пользователя: {self.user.email} - {self.user.id}'

<<<<<<< HEAD
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.userprofile.save()

=======
>>>>>>> CN-26
    @property
    def age(self):
        if self.user.birthday:
            today = now()
            return today.year - self.user.birthday.year - (
                    (today.month, today.day) < (self.user.birthday.month, self.user.birthday.day))
        return 0

    @property
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
