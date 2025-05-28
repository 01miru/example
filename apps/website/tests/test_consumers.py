import pytest
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from channels.testing import WebsocketCommunicator
from django.contrib.auth import get_user_model

from config.asgi import application

User = get_user_model()


@database_sync_to_async
def create_user(**kwargs):
    return User.objects.create_user(**kwargs)


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_user_cannot_connect_with_other_user_id():
    user = await create_user(username="testuser", password="testpass")

    communicator = WebsocketCommunicator(
        application, f"/ws/notifications/{user.id + 1}/"
    )
    communicator.scope["user"] = user

    connected, _ = await communicator.connect()
    assert not connected


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_user_can_connect_to_own_channel():
    user = await create_user(username="testuser2", password="testpass")

    communicator = WebsocketCommunicator(application, f"/ws/notifications/{user.id}/")
    communicator.scope["user"] = user

    connected, _ = await communicator.connect()
    assert connected

    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_user_receives_report_ready_notification():
    user = await create_user(username="testuser3", password="testpass")

    communicator = WebsocketCommunicator(application, f"/ws/notifications/{user.id}/")
    communicator.scope["user"] = user

    connected, _ = await communicator.connect()
    assert connected

    channel_layer = get_channel_layer()
    await channel_layer.group_send(
        f"user_{user.id}",
        {"type": "send_report_ready", "report_url": "/media/reports/report_test.pdf"},
    )

    response = await communicator.receive_json_from()
    assert response["message"] == "Raport jest gotowy do pobrania."
    assert response["report_url"] == "/media/reports/report_test.pdf"

    await communicator.disconnect()
