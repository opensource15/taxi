# https://velog.io/@wodnr_09/Django-%EC%8B%A4%EC%8B%9C%EA%B0%84-%EC%B1%84%ED%8C%85-%ED%8A%9C%ED%86%A0%EB%A6%AC%EC%96%BC

from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.chat_group_name = f'chat_{self.chat_id}'
        self.username = self.scope['user'].username

        # 그룹에 join
        # send 등 과 같은 동기적인 함수를 비동기적으로 사용하기 위해서는 async_to_sync 로 감싸줘야함
        # Join room group
        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name
        )
        # WebSocket 연결
        await self.accept()

    async def disconnect(self, close_code):
        # 그룹에서 Leave
        # Leave room group
        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name
        )
    # WebSocket 에게 메세지 receive
    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # room group 에게 메세지 send
        # Send message to room group
        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'chat_message',
                'username' : self.username,
                'message': message
            }
        )
    # room group 에서 메세지 receive
    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        
        # WebSocket 에게 메세지 전송
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'username' : username,
            'message': message
        }))