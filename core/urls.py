from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers, serializers, viewsets
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.routers import DefaultRouter
from . import views


urlpatterns = [
    path('current-user/', views.current_user),
    path('users/', views.UserAuthentication.as_view()),
    path('retro-board-items/', views.RetroBoardItemsList.as_view()),
    path('session-owner/', views.check_session_owner),
    path('deploy/', views.test_deploy)
]
