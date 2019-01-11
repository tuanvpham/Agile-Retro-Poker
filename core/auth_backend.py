from django.contrib.auth.backends import ModelBackend

from .models import User


class EmailPasswordlessAuthBackend(ModelBackend):
    def authenticate(self, request, username=None):
        try:
            return User.objects.get(email=username)
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
