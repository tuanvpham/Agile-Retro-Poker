from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email',)


class UserSerializerWithToken(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    def get_token(self, obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ('token', 'email', 'username')


class SessionSerializer(serializers.ModelSerializer):
    owner_id = serializers.SerializerMethodField()
    owner_username = serializers.SerializerMethodField()
    owner_email = serializers.SerializerMethodField()

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
            'id',
            'title',
            'description',
            'session_type',
            'owner_id',
            'owner_username',
            'owner_email'
        )


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


class SessionMemberSerializer(serializers.ModelSerializer):
    session_member_id = serializers.SerializerMethodField()
    session_member_username = serializers.SerializerMethodField()
    session_member_email = serializers.SerializerMethodField()

    def get_session_member_id(self, obj):
        try:
            session_member = User.objects.get(id=obj.member.id)
            session_member_id = session_member.id
        except User.DoesNotExist:
            session_member_id = -1
        return session_member_id

    def get_session_member_username(self, obj):
        try:
            session_member = User.objects.get(id=obj.member.id)
            session_member_username = session_member.username
        except User.DoesNotExist:
            session_member_username = ''
        return session_member_username

    def get_session_member_email(self, obj):
        try:
            session_member = User.objects.get(id=obj.member.id)
            session_member_email = session_member.email
        except User.DoesNotExist:
            session_member_email = ''
        return session_member_email

    class Meta:
        model = SessionMember
        fields = (
            'id',
            'session',
            'session_member_id',
            'session_member_username',
            'session_member_email'
        )


class StorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Story
        fields = ('id', 'title', 'description', 'story_points', 'session')
