from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from .models import *


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email',)


class UserSerializerWithToken(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    def get_token(self, obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ('token', 'email', 'username', 'password')


class SessionSerializer(serializers.ModelSerializer):
    session_owner_id = serializers.SerializerMethodField(
        'get_owner_id'
    )
    session_owner_username = serializers.SerializerMethodField(
        'get_owner_username'
    )
    session_owner_email = serializers.SerializerMethodField(
        'get_owner_email'
    )

    def create(self, validated_data):
        request = self._context.get("request")
        session = Session.objects.create(
            **validated_data,
            owner=request.user
        )
        session.save()
        return session

    def get_owner_id(self, obj):
        try:
            owner_obj = User.objects.get(id=obj.owner.id)
            owner_id = owner_obj.id
        except User.DoesNotExist:
            owner_id = -1
        return owner_id

    def get_owner_username(self, obj):
        try:
            owner_obj = User.objects.get(id=obj.owner.id)
            owner_username = owner_obj.username
        except User.DoesNotExist:
            owner_username = ''
        return owner_username

    def get_owner_email(self, obj):
        try:
            owner_obj = User.objects.get(id=obj.owner.id)
            owner_email = owner_obj.email
        except User.DoesNotExist:
            owner_email = ''
        return owner_email

    class Meta:
        model = Session
        fields = (
            'id', 'title', 'description',
            'session_type', 'session_owner_id', 'session_owner_username',
            'session_owner_email'
        )


class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = ('id', 'title', 'description', 'story_points', 'session')
