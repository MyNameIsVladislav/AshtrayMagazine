from django.db import models

from core.settings import AUTH_USER_MODEL


class PurseModel(models.Model):
    class Meta:
        unique_together = (("user_id", "id"),)
        # permissions = (("add_money", "Top up balance"),)

    user_id = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='money', verbose_name='user')
    money = models.PositiveIntegerField(verbose_name='money', default=0)

    def __str__(self):
        return f'{self.user_id.last_name} - {self.money}'

    @property
    def full_name(self):
        return f'{self.user_id.first_name} {self.user_id.last_name}'
