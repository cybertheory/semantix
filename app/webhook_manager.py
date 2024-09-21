import aiohttp
from database import Webhook, get_db
from logger import app_logger

async def get_active_webhooks():
    db = next(get_db())
    return db.query(Webhook).filter(Webhook.is_active == True).all()

async def send_webhook(webhook, payload):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(webhook.url, json=payload) as response:
                app_logger.info(f"Webhook sent to {webhook.url} with status {response.status}")
                return response.status
        except Exception as e:
            app_logger.error(f"Error sending webhook to {webhook.url}: {str(e)}")
            return None

async def process_webhooks(notification):
    webhooks = await get_active_webhooks()
    for webhook in webhooks:
        status = await send_webhook(webhook, notification)
        print(f"Webhook {webhook.url} processed with status {status}")
