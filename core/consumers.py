from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import *
from .utilities import *
import json


class SessionConsumer(WebsocketConsumer):
    def connect(self):
        print('CONNECT')
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
            print('DISCONNECT')
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
        item_type = text_data_json['itemType']
        item_text = text_data_json['itemText']

        session = get_session_object(
            self.scope['url_route']['kwargs']['session_name']
        )

        if item_type == 'what_went_well':
            retro_board_item = RetroBoardItems.objects.create(
                owner=self.scope['user'],
                session=session,
                item_type='WWW',
                item_text=item_text
            )
            retro_board_item.save()
        elif item_type == 'what_did_not':
            retro_board_item = RetroBoardItems.objects.create(
                owner=self.scope['user'],
                session=session,
                item_type='WDN',
                item_text=item_text
            )
            retro_board_item.save()
        else:
            retro_board_item = RetroBoardItems.objects.create(
                owner=self.scope['user'],
                session=session,
                item_type='AI',
                item_text=item_text
            )
            retro_board_item.save()

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'send_out_retro_board_item_to_websocket',
                'item_id': retro_board_item.id,
                'item_owner': self.scope['user'].username,
                'item_type': retro_board_item.item_type,
                'item_text': item_text
            }
        )

    def send_out_retro_board_item_to_websocket(self, event):
        item_id = event['item_id']
        item_owner = event['item_owner']
        item_type = event['item_type']
        item_text = event['item_text']

        self.send(text_data=json.dumps({
            'item_id': item_id,
            'item_owner': item_owner,
            'item_type': item_type,
            'item_text':  item_text
        }))
