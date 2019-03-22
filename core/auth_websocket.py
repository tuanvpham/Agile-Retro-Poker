from django.db import close_old_connections
from django.conf import settings
from core.models import User


def get_object(email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None


class QueryEmailAuthMiddlewareStack:
    """
    Custom middleware (insecure) that takes username from the query string.
    """

    def __init__(self, inner):
        # Store the ASGI application we were passed
        self.inner = inner

    def __call__(self, scope):
        email_query = scope['query_string'].decode()
        user = get_object(email_query)
        close_old_connections()

        return self.inner(dict(scope, user=user))
