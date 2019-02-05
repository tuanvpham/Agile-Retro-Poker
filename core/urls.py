from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers, serializers, viewsets
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()


urlpatterns = [
    path('current-user/', views.current_user),
    path('users/', views.UserAuthentication.as_view()),
    path('sessions/', views.SessionCreate.as_view()),
    path('session-members/', views.SessionMemberList.as_view()),
    path('deploy/', views.test_deploy)
]
