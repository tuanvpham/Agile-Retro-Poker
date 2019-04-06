from django.shortcuts import get_object_or_404
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import *
from .utilities import *
import json


class HomeConsumer(WebsocketConsumer):
    def connect(self):
        print('CONNECT')
        self.room_name = 'dashboard'
        self.room_group_name = 'dashboard_home'
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        print('DISCONNECT')
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if 'create_session' in text_data_json:
            session_type = text_data_json['session_type']
            entered_text = text_data_json['entered_text']
            session_id = text_data_json['session_id']
            owner = text_data_json['owner_username']
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'create_session',
                    'session_type': session_type,
                    'entered_text': entered_text,
                    'session_id': session_id,
                    'owner': owner
                }
            )
        elif 'create_session_kate' in text_data_json:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'create_session_kate',
                }
            )
        elif 'delete_session' in text_data_json:
            session_id = text_data_json['session_id']
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'delete_session',
                    'session_id': session_id
                }
            )
        elif 'delete_session_kate' in text_data_json:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'delete_session_kate',
                }
            )
        elif 'close_socket' in text_data_json:
            self.close()

    def create_session(self, event):
        session_type = event['session_type']
        entered_text = event['entered_text']
        session_id = event['session_id']
        owner = event['owner']
        self.send(text_data=json.dumps({
            'create_session': 'Create a new session',
            'session_type': session_type,
            'entered_text': entered_text,
            'session_id': session_id,
            'owner': owner
        }))

    def create_session_kate(self, event):
        self.send(text_data=json.dumps({
            'create_session': 'Create a new session',
        }))

    def delete_session(self, event):
        session_id = event['session_id']
        self.send(text_data=json.dumps({
            'delete_session': 'Delete a session',
            'session_id': session_id
        }))
    
    def delete_session_kate(self, event):
        self.send(text_data=json.dumps({
            'delete_session': 'Delete a session',
        }))


class RetroConsumer(WebsocketConsumer):
    def connect(self):
        print('CONNECT')
        session = get_session_object(
            self.scope['url_route']['kwargs']['session_name']
        )

        if session is not None:
            self.room_name = session.title
            self.room_group_name = 'session_%s' % self.room_name

            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )
            self.accept()
        else:
            self.close()

    def disconnect(self, close_code):
        # Leave session
        print('DISCONNECT - WEBSOCKET CLOSED')
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        is_mobile = False
        user = None
        if 'user_email' in text_data_json:
            is_mobile = True
            user = get_user_object(text_data_json['user_email'])

        if 'end_session' in text_data_json:
            session = get_session_object(
                self.scope['url_route']['kwargs']['session_name']
            )
            owner = User.objects.get(id=session.owner_id)

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'end_session_by_owner',
                    'session_owner': owner.username,
                    'message': text_data_json['end_session']
                }
            )
        elif 'exit_session' in text_data_json:
            member = User.objects.get(
                username=text_data_json['session_member']
            )
            session = get_session_object(
                self.scope['url_route']['kwargs']['session_name']
            )
            session_member = SessionMember.objects.get(
                session=session.id,
                member=member.id
            )

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'exit_session_by_user',
                    'member': member.username,
                    'message': text_data_json['exit_session']
                }
            )

            session_member.delete()
        elif 'newItemText' in text_data_json:
            item_type = text_data_json['itemType']
            item_text = text_data_json['itemText']
            new_item_text = text_data_json['newItemText']
            item_id = text_data_json['item_id']
            item_index = text_data_json['index']
            session = get_session_object(
                self.scope['url_route']['kwargs']['session_name']
            )
            RetroBoardItems.objects.filter(
                owner=self.scope['user'],
                session=session,
                item_type=item_type,
                item_text=item_text,
                id=item_id
            ).update(item_text=new_item_text)

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'send_out_new_item_text',
                    'item_id': item_id,
                    'item_type': item_type,
                    'new_item_text': new_item_text,
                    'item_index': item_index
                }
            )
        elif 'delete' in text_data_json:
            item_type = text_data_json['itemType']
            item_text = text_data_json['itemText']
            item_id = text_data_json['item_id']
            session = get_session_object(
                self.scope['url_route']['kwargs']['session_name']
            )
            RetroBoardItems.objects.filter(
                owner=self.scope['user'],
                session=session,
                item_type=item_type,
                item_text=item_text,
                id=item_id
            ).delete()

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'delete_item_from_front_end',
                    'item_id': item_id,
                    'item_type': item_type
                }
            )
        else:
            item_type = text_data_json['itemType']
            item_text = text_data_json['itemText']

            session = get_session_object(
                self.scope['url_route']['kwargs']['session_name']
            )

            if is_mobile:
                if user is not None:
                    owner = user
                else:
                    print("User does not exist")
            else:
                owner = self.scope['user']

            if item_type == 'what_went_well':
                retro_board_item = RetroBoardItems.objects.create(
                    owner=owner,
                    session=session,
                    item_type='WWW',
                    item_text=item_text
                )
                retro_board_item.save()
            elif item_type == 'what_did_not':
                retro_board_item = RetroBoardItems.objects.create(
                    owner=owner,
                    session=session,
                    item_type='WDN',
                    item_text=item_text
                )
                retro_board_item.save()
            else:
                retro_board_item = RetroBoardItems.objects.create(
                    owner=owner,
                    session=session,
                    item_type='AI',
                    item_text=item_text
                )
                retro_board_item.save()

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'send_out_retro_board_item_to_websocket',
                    'item_id': retro_board_item.id,
                    'item_owner': owner.username,
                    'item_type': retro_board_item.item_type,
                    'item_text': item_text,
                    'session': self.scope['url_route']['kwargs']['session_name']
                }
            )

    def send_out_new_item_text(self, event):
        item_id = event['item_id']
        item_type = event['item_type']
        new_item_text = event['new_item_text']
        item_index = event['item_index']

        self.send(text_data=json.dumps({
            'id': item_id,
            'item_type': item_type,
            'new_item_text': new_item_text,
            'edit_item_message': 'edit_item',
            'item_index': item_index
        }))

    def delete_item_from_front_end(self, event):
        item_id = event['item_id']
        item_type = event['item_type']

        self.send(text_data=json.dumps({
            'id': item_id,
            'item_type': item_type,
            'delete_item_message': 'delete_item'
        }))

    def send_out_retro_board_item_to_websocket(self, event):
        item_id = event['item_id']
        item_owner = event['item_owner']
        item_type = event['item_type']
        item_text = event['item_text']
        session = event['session']

        self.send(text_data=json.dumps({
            'id': item_id,
            'item_owner': item_owner,
            'item_type': item_type,
            'item_text':  item_text,
            'session': session
        }))

    def end_session_by_owner(self, event):
        end_session_message = event['message']
        session_owner = event['session_owner']
        self.send(text_data=json.dumps({
            'session_owner': session_owner,
            'end_session_message': end_session_message
        }))
        self.close()

    def exit_session_by_user(self, event):
        exit_session_message = event['message']
        member = event['member']
        self.send(text_data=json.dumps({
            'member': member,
            'exit_session_message': exit_session_message
        }))
        self.close()


class PokerConsumer(WebsocketConsumer):
    def connect(self):
        print('CONNECT')
        session = get_session_object(
            self.scope['url_route']['kwargs']['session_name']
        )

        if session is not None:
            self.room_name = session.title
            self.room_group_name = 'session_%s' % self.room_name

            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )
            self.accept()
        else:
            self.close()

    def disconnect(self, close_code):
        # Leave session
        print('DISCONNECT - WEBSOCKET CLOSED')
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if 'next_story' in text_data_json:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'toggle_next_story',
                    'toggle_next_story': text_data_json['next_story']
                }
            )
        elif 'prev_story' in text_data_json:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'toggle_prev_story',
                    'toggle_prev_story': text_data_json['prev_story']
                }
            )
        elif 'play_card' in text_data_json:
            session = get_session_object(
                self.scope['url_route']['kwargs']['session_name']
            )
            story = get_story_object(text_data_json['story'])
            player = get_user_object(text_data_json['player'])

            try:
                lookUpCard = Card.objects.get(
                    session=session,
                    owner=self.scope['user'],
                    story=story
                )
            except Card.DoesNotExist:
                lookUpCard = None

            if lookUpCard is None:
                card = Card.objects.create(
                    card=text_data_json['card'],
                    session=session,
                    owner=self.scope['user'],
                    story=story
                )
                card.save()
            else:
                lookUpCard.card = text_data_json['card']
                lookUpCard.save()

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'play_card',
                    'play_card': text_data_json['play_card'],
                    'card': text_data_json['card'],
                    'player': player.username
                }
            )
        elif 'flip_card' in text_data_json:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'flip_card',
                    'flip_card': text_data_json['flip_card'],
                }
            )
        elif 'submit_points' in text_data_json:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'submit_new_story_points',
                    'submit_points': text_data_json['submit_points'],
                    'points': text_data_json['points'],
                    'story': text_data_json['story']
                }
            )
        elif 'reset_cards' in text_data_json:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'reset_cards',
                    'reset_cards': text_data_json['reset_cards'],
                    'story': text_data_json['story']
                }
            )
        elif 'end_game' in text_data_json:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'end_game',
                    'end_game': text_data_json['end_game'],
                    'story': text_data_json['story']
                }
            )
        elif 'close_socket' in text_data_json:
            self.close()

    def toggle_next_story(self, event):
        toggle_next_story = event['toggle_next_story']
        self.send(text_data=json.dumps({
            'toggle_next_story': toggle_next_story
        }))

    def toggle_prev_story(self, event):
        toggle_prev_story = event['toggle_prev_story']
        self.send(text_data=json.dumps({
            'toggle_prev_story': toggle_prev_story
        }))

    def play_card(self, event):
        play_card = event['play_card']
        card = event['card']
        player = event['player']
        self.send(text_data=json.dumps({
            'play_card': play_card,
            'player': player,
            'card': card
        }))

    def flip_card(self, event):
        flip_card = event['flip_card']
        self.send(text_data=json.dumps({
            'flip_card': flip_card,
        }))

    def submit_new_story_points(self, event):
        submit_points = event['submit_points']
        points = event['points']
        story = event['story']
        self.send(text_data=json.dumps({
            'submit_points': submit_points,
            'points': points,
            'story': story
        }))

    def reset_cards(self, event):
        reset_cards = event['reset_cards']
        story = event['story']
        self.send(text_data=json.dumps({
            'reset_cards': reset_cards,
            'story': story
        }))

    def end_game(self, event):
        end_game = event['end_game']
        story = event['story']
        self.send(text_data=json.dumps({
            'end_game': end_game,
            'story': story
        }))
        self.close()


class LobbyConsumer(WebsocketConsumer):
    def connect(self):
        session = get_session_object(
            self.scope['url_route']['kwargs']['session_name']
        )

        if session is not None and session.is_started is False:
            self.room_name = session.title
            self.room_group_name = 'session_%s' % self.room_name

            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )
            self.accept()
        else:
            self.close()

    def disconnect(self, close_code):
        # Leave session
        print('DISCONNECT - WEBSOCKET CLOSED')
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        session = get_session_object(
            self.scope['url_route']['kwargs']['session_name']
        )
        if 'has_joined' in text_data_json:
            has_joined = text_data_json['has_joined']
            player = text_data_json['player']
            try:
                user = User.objects.get(email=player)
            except User.DoesNotExist:
                user = None

            if user is not None:
                try:
                    member = SessionMember.objects.get(
                        session=session,
                        member=user
                    )
                except SessionMember.DoesNotExist:
                    member = None

                if member is not None:
                    has_joined = 'User already joined the session'
                else:
                    has_joined = 'New player joined the session'
                    new_member = SessionMember.objects.create(
                        session=session, member=user
                    )
                    new_member.save()

                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'has_joined',
                        'has_joined': has_joined,
                        'player': user.username
                    }
                )
            else:
                print("User does not exist!")
        elif 'start_game' in text_data_json:
            start_game = text_data_json['start_game']
            session.is_started = True
            session.save(update_fields=['is_started'])
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'start_game',
                    'start_game': start_game
                }
            )
        elif 'display_retro' in text_data_json:
            display_retro = text_data_json['display_retro']
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'display_retro',
                    'display_retro': display_retro
                }
            )
        elif 'cancel_game' in text_data_json:
            cancel_game = text_data_json['cancel_game']
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'cancel_game',
                    'cancel_game': cancel_game
                }
            )
        elif 'exit_game' in text_data_json:
            exit_game = text_data_json['exit_game']
            player = text_data_json['player']
            try:
                user = User.objects.get(email=player)
            except User.DoesNotExist:
                user = None

            if user is not None:
                try:
                    member = SessionMember.objects.get(
                        session=session,
                        member=user
                    )
                except SessionMember.DoesNotExist:
                    member = None

                if member is not None:
                    member = SessionMember.objects.get(
                        session=session,
                        member=user
                    )
                    member.delete()
                    exit_game = 'User has left the session'
                else:
                    exit_game = 'There is no user like this in session'

                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'exit_game',
                        'exit_game': exit_game,
                        'player': user.username
                    }
                )
            else:
                print('User does not exist')

    def has_joined(self, event):
        has_joined = event['has_joined']
        player = event['player']
        self.send(text_data=json.dumps({
            'has_joined': has_joined,
            'player': player
        }))

    def start_game(self, event):
        start_game = event['start_game']
        self.send(text_data=json.dumps({
            'start_game': start_game
        }))
        self.close()

    def display_retro(self, event):
        display_retro = event['display_retro']
        self.send(text_data=json.dumps({
            'display_retro': display_retro
        }))

    def cancel_game(self, event):
        cancel_game = event['cancel_game']
        self.send(text_data=json.dumps({
            'cancel_game': cancel_game
        }))

    def exit_game(self, event):
        exit_game = event['exit_game']
        player = event['player']
        self.send(text_data=json.dumps({
            'exit_game': exit_game,
            'player': player
        }))
