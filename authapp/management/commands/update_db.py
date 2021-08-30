from django.core.management.base import BaseCommand

from ...models import CustomUser, UserProfile


class Command(BaseCommand):
    def handle(self, *args, **options):
        users = CustomUser.objects.all()
        for user in users:
            users_profile = UserProfile.objects.create(user=user)
            users_profile.save()
