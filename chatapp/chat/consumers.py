# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .consumer_helpers import save_user_channel_name, set_user_offline, get_user_channel_name, save_chat


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user_id = None

    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        await self.accept()
        await save_user_channel_name(user_id=self.user_id, channel_name=self.channel_name)

    async def disconnect(self, close_code):
        await set_user_offline(user_id = self.user_id)

    async def receive(self, text_data=None):
        """
        sample body:

        user 1 = {
        "message": "I'm user 1",
        "sender": "shadowmonarch",
        "send_to": 5
        }

        user 2 = {
        "message": "I'm user 2",
        "sender": "newuser",
        "send_to": 6
        }
        
        """
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        receiver_id = text_data_json["send_to"]
        send_to = await get_user_channel_name(receiver_id)

        if send_to: #Send the message to websocket
            await self.channel_layer.send(
                send_to,
                {
                    'type' : 'chatroom.message',
                    'message' : message,
                    'receiver_id' : receiver_id,
                    'sender_id' : self.user_id
                }
            )
        
        else:
            print("Somthing went wrong at consumer receive method!")

    async def chatroom_message(self, event):

        # Sends message over websocket
        await self.send(
            text_data=json.dumps(
                {
                    'message': event['message'],
                    'sender_id': event['sender_id'],
                    # we can add more things here
                }
            )
        )

        # Saving message to DB
        await save_chat(event)