from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers, serializers, viewsets
from rest_framework_jwt.views import obtain_jwt_token


from . import views

urlpatterns = [
    path('token-auth/', obtain_jwt_token),
    path('current_user/', views.current_user),
    path('users/', views.UserList.as_view()),
    path('deploy/', views.test_deploy)
]
