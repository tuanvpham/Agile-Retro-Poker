from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers, serializers, viewsets
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()


urlpatterns = [
    path('login/', views.Login.as_view()),
    path('oauth_user/', views.oauth_user),
    path('current-user/', views.current_user),
    path('sessions/', views.SessionCreate.as_view()),
    path('delete_session/', views.delete_session),
    path('retro-board-items/', views.RetroBoardItemsList.as_view()),
    path('stories/', views.StoryItemList.as_view()),
    path('story_select/', views.StorySelectList.as_view()),
    path('session-owner/', views.check_session_owner),
    path('session-members/<int:session_id>/', views.SessionMemberList.as_view()),
    path('end_retro/', views.end_retro),
    path('end_poker/', views.end_poker),
    path('update_points/', views.update_points),
    path('stories/<int:session_id>/', views.Stories.as_view()),
    path('session-started/', views.check_session_started),
    path('remove_stories/', views.remove_stories),
    path('cards/<int:session_id>/<int:story_id>/', views.Cards.as_view())
]
