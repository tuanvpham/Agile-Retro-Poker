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
        print(email_query)

        # print(type(scope['query_string'].decode()))
        # Look up user from query string (you should also do things like
        # check it's a valid user ID, or if scope["user"] is already populated)
        # user = User.objects.get(email=email_query)
        user = get_object(email_query)
        close_old_connections()
        # Return the inner application directly and let it run everything else
        return self.inner(dict(scope, user=user))
