import time
from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer


@shared_task
def generate_report(user_id):
    time.sleep(5)
    report_url = f"/media/reports/report_{user_id}.pdf"

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{user_id}",
        {
            "type": "send_report_ready",
            "report_url": report_url,
        },
    )
