from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import *
from .utilities import *
import json


class SessionConsumer(WebsocketConsumer):
    def connect(self):
        print(self.scope['url_route']['kwargs']['session_name'])
        session = get_session_object(
            self.scope['url_route']['kwargs']['session_name']
        )
        user = get_session_member_object(self.scope['user'])
        if session and self.scope['user'] is not None:
            self.room_name = session.title
            self.room_group_name = 'session_%s' % self.room_name

            if user is None:
                new_member = SessionMember.objects.create(
                    session=session, member=self.scope['user']
                )
                new_member.save()

            # Join session
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )

            self.accept()
        else:
            self.close()

    def disconnect(self, close_code):
        # Leave session
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json)
        message = text_data_json['actionItemText']

        session = get_session_object(
            self.scope['url_route']['kwargs']['session_name']
        )
        retro_action_item = RetroActionItems.objects.create(
            owner=self.scope['user'],
            session=session,
            action_item_text=message
        )
        retro_action_item.save()

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from session
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        # self.send(text_data=json.dumps({
        #     'message': message
        # }))
        self.send(text_data=message)
