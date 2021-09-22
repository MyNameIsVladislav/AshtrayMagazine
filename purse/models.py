from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from core.settings import AUTH_USER_MODEL


class PurseModel(models.Model):
    class Meta:
        unique_together = (("user_id", "id"),)
        permissions = (("add_money", "Top up balance"),)

    user_id = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   related_name='wallet', verbose_name='user')
    money = models.PositiveIntegerField(verbose_name='money', default=0)

    def __str__(self):
        return f'{self.user_id.last_name} - {self.money}'

    @property
    def full_name(self):
        return f'{self.user_id.first_name} {self.user_id.last_name}'


@receiver(post_save, sender=AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        PurseModel.objects.create(user_id=instance)


@receiver(post_save, sender=AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.wallet.save()
