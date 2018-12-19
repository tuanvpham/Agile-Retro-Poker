from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from jira import JIRA, JIRAError
from rest_framework import viewsets, authentication, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import Session, Role, Story, User
from .serializers import *


# Rest API
@api_view(['POST'])
def login_view(request):
    """
    Login API: input login data from clients
    """
    if request.method == 'POST':
        email = request.data['user']['email']
        password = request.data['user']['password']
        try:
            jac = JIRA(
                'https://agilecommand.atlassian.net',
                basic_auth=(email, password)
            )
            jac_username = jac.myself().get('displayName')
            user = authenticate(request, username=email)
            if user is None:
                user = User(
                    email=email, username=jac_username, password=password
                )
                user.save()
            login(request, user)
            return Response(status=status.HTTP_201_CREATED)
        except JIRAError as e:
            print('This is jira error: ' + str(e.status_code))
            return Response(status=status.HTTP_400_BAD_REQUEST)


# @login_required(login_url='/')
# def dashboard(request):
#     return render(request, 'dashboard.html')


# @login_required(login_url='/')
# def logout_view(request):
#     logout(request)
#     return redirect('core:login_view')


# Rest API for clients
class UserView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['post', 'head', 'options']
