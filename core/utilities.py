from rest_framework_jwt.settings import api_settings

from .models import *


def get_user_object(email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None


def get_session_object(title):
        try:
            return Session.objects.get(title=title)
        except Session.DoesNotExist:
            return None


def get_story_object(id):
    try:
        return Story.objects.get(id=id)
    except Story.DoesNotExist:
        return None


def get_session_member_object(user):
    try:
        return SessionMember.objects.get(member=user)
    except SessionMember.DoesNotExist:
        return None


def my_jwt_response_handler(token, user=None, request=None):
    '''
        Return response includes token, email, username
    '''

    return {
        'token': token,
        'user': UserSerializer(user, context={'request': request}).data
    }


def generate_new_token(user):
    '''
        Return token for authenticated user
    '''
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    return token
