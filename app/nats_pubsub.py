import asyncio
import json
from logger import app_logger
import nats
from config import Config
from embeddings import get_embedding
from vector_search import search_similar_embeddings, store_embedding
from database import Subscription, get_db
from webhook_manager import process_webhooks

class NATSClient:
    def __init__(self):
        self.nc = None  # NATS client connection

    async def connect(self):
        """
        Connect to the NATS server.
        """
        self.nc = await nats.connect(Config.NATS_SERVER_URL)
        print(f"Connected to NATS at {Config.NATS_SERVER_URL}")

    async def close(self):
        """
        Close the NATS connection.
        """
        if self.nc:
            await self.nc.close()
            print("Closed NATS connection")

    async def handle_user_subscription(self, user_id, user_query):
        """
        Handle a new user subscription.
        """
        # Generate embedding for the user's query
        query_embedding = get_embedding(user_query)

        # Store the user's query embedding in the vector database
        user_subject = f"user_{user_id}"
        metadata = {
            "user_id": user_id,
            "user_subject": user_subject,
            "user_query": user_query
        }
        store_embedding(query_embedding, metadata)

        # Store subscription in PostgreSQL
        db = next(get_db())
        new_subscription = Subscription(user_id=user_id, query=user_query, metadata=metadata)
        db.add(new_subscription)
        db.commit()

        app_logger.info(f"Stored subscription for user '{user_id}' with subject '{user_subject}'")

    async def process_notification(self, notification_text):
        """
        Process an incoming notification.
        """
        # Generate embedding for the notification
        notification_embedding = get_embedding(notification_text)

        # Perform semantic search to find matching user subscriptions
        matching_subscriptions = search_similar_embeddings(
            notification_embedding,
            threshold=Config.SIMILARITY_THRESHOLD
        )

        # Publish the notification to each matching user's subject
        for subscription in matching_subscriptions:
            user_subject = subscription.get('user_subject')
            await self.nc.publish(user_subject, notification_text.encode())
            print(f"Published notification to subject '{user_subject}'")

        # Process webhooks
        await process_webhooks({"text": notification_text, "matching_users": len(matching_subscriptions)})

        app_logger.info(f"Published notification to {len(matching_subscriptions)} subjects")
