from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers, serializers, viewsets
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'sessions', views.SessionViewSet, basename='session')


urlpatterns = [
    path('current-user/', views.current_user),
    path('users/', views.UserAuthentication.as_view()),
    path('sessions/', views.SessionCreate.as_view()), 
    url(r'^', include(router.urls)),
    path('deploy/', views.test_deploy)
]
