import json
from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = int(self.scope["url_route"]["kwargs"]["user_id"])
        self.user = self.scope["user"]

        if not self.user.is_authenticated or self.user.id != self.user_id:
            await self.close()
            return

        self.group_name = f"user_{self.user_id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_report_ready(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "message": "Raport jest gotowy do pobrania.",
                    "report_url": event["report_url"],
                }
            )
        )
