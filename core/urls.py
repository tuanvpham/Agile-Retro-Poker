from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers, serializers, viewsets

from . import views
app_name = 'core'
# router = routers.DefaultRouter()
# router.register('users', views.login_view)

urlpatterns = [
    # path('', views.login_view, name='login_view'),
    # path('dashboard/', views.dashboard, name='dashboard'),
    # path('logout/', views.logout_view, name='logout_view'),
    # Restful API
    # path('api/', include(router.urls)),
    url(r'^api/users/login', views.login_view),
    # path('api/login', views.login_view, name='login_view'),
]
