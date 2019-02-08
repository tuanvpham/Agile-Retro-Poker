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
    class Meta:
        model = Session
        fields = ('id', 'title')


class RetroActionItemsSerializer(serializers.ModelSerializer):
    owner_username = serializers.SerializerMethodField()

    def get_owner_username(self, obj):
        try:
            owner_obj = User.objects.get(id=obj.owner.id)
            owner_username = owner_obj.username
        except User.DoesNotExist:
            owner_username = ''
        return owner_username

    class Meta:
        model = RetroActionItems
        fields = ('id', 'owner_username', 'action_item_text')


class RetroWhatWentWellSerializer(serializers.ModelSerializer):
    owner_username = serializers.SerializerMethodField()

    def get_owner_username(self, obj):
        try:
            owner_obj = User.objects.get(id=obj.owner.id)
            owner_username = owner_obj.username
        except User.DoesNotExist:
            owner_username = ''
        return owner_username

    class Meta:
        model = RetroWhatWentWell
        fields = ('id', 'owner_username', 'what_went_well_text')


class RetroWhatWentWellSerializer(serializers.ModelSerializer):
    owner_username = serializers.SerializerMethodField()

    def get_owner_username(self, obj):
        try:
            owner_obj = User.objects.get(id=obj.owner.id)
            owner_username = owner_obj.username
        except User.DoesNotExist:
            owner_username = ''
        return owner_username

    class Meta:
        model = RetroWhatWentWell
        fields = ('id', 'owner_username', 'what_went_well_text')


class RetroBoardItemsSerializer(serializers.ModelSerializer):
    owner_username = serializers.SerializerMethodField()
    session_title = serializers.SerializerMethodField()

    def get_owner_username(self, obj):
        try:
            owner_obj = User.objects.get(id=obj.owner.id)
            owner_username = owner_obj.username
        except User.DoesNotExist:
            owner_username = ''
        return owner_username

    def get_session_title(self, obj):
        try:
            session_obj = Session.objects.get(id=obj.session.id)
            session_title = session_obj.title
        except Session.DoesNotExist:
            session_title = ''
        return session_title

    class Meta:
        model = RetroBoardItems
        fields = (
            'id',
            'owner_username',
            'session_title',
            'item_type',
            'item_text'
        )


class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = ('id', 'title', 'description', 'story_points', 'session')
