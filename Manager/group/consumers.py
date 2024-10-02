import json
from channels.generic.websocket import AsyncWebsocketConsumer


class SignallingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'room_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        content = json.loads(text_data)

        if content['action'] == 'join':
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'join.message',
                'username': content['username']
            })

        elif content['action'] == 'offer':
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'offer.message',
                'offer': content['offer'],
                'username': content['username']
            })

        elif content['action'] == 'answer':
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'answer.message',
                'answer': content['answer'],
                'username': content['username']
            })

        elif content['action'] == 'candidate':
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'candidate.message',
                'candidate': content['candidate'],
                'username': content['username']

            })

    async def join_message(self, event):
        await self.send(json.dumps({
            'action': 'join',
            'username': event['username']
        }))

    async def offer_message(self, event):
        await self.send(json.dumps({
            'action': 'offer',
            'offer': event['offer'],
            'username': event['username']
        }))

    async def answer_message(self, event):
        await self.send(json.dumps({
            'action': 'answer',
            'answer': event['answer'],
            'username': event['username']
        }))

    async def candidate_message(self, event):
        await self.send(json.dumps({
            'action': 'candidate',
            'candidate': event['candidate'],
            'username': event['username']

        }))
