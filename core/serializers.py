from rest_framework.serializers import ModelSerializer
from .models import Session, Role, User, Story


class SessionSerializer(ModelSerializer):
    class Meta:
        model = Session
        fields = ('id', 'title')


class RoleSerializer(ModelSerializer):
    class Meta:
        model = Role
        fields = ('id', 'title')


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password')


class StorySerializer(ModelSerializer):
    class Meta:
        model = Story
        fields = ('id', 'title', 'description', 'story_points', 'session')
