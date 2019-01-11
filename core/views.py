from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required

from jira import JIRA, JIRAError
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings

from .models import *
from .serializers import *


# Rest API View
@api_view(['GET'])
def current_user(request):
    '''
    Determine the current user by their token, and return their data
    '''

    serializer = UserSerializer(request.user)
    return Response(serializer.data)


class UserList(APIView):
    '''
    Login with Jira Auth
    If user exists in database, return user data and new token
    Else create new user and return user data
    '''

    permission_classes = (AllowAny,)

    def get_object(self, email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None

    def post(self, request, format=None):
        email = request.data['email']
        password = request.data['password']
        try:
            # Login with Jira Auth
            jac = JIRA(
                'https://agilecommandcentralgroup10.atlassian.net',
                basic_auth=(email, password)
            )
            jac_username = jac.myself().get('displayName')
            user = self.get_object(email)
            if user is None:
                # Signup with ACC
                serializer = UserSerializerWithToken(data={
                    'email': email,
                    'username': jac_username,
                    'password': password
                })
                if serializer.is_valid():
                    serializer.save()
                    return Response(
                        serializer.data,
                        status=status.HTTP_201_CREATED
                    )
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                token = generate_new_token(user)
                user_existed_data = {
                    'token': token,
                    'email': user.email,
                    'username': user.username
                }
                return Response(
                    user_existed_data,
                    status=status.HTTP_200_OK
                )
        except JIRAError as e:
            return Response(status=status.HTTP_408_REQUEST_TIMEOUT)


# Test deploy
@api_view(['GET'])
@permission_classes((AllowAny, ))
def test_deploy(request):
    return HttpResponse(content='You made it')


# Utitlities
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
