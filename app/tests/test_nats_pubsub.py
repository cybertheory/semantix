import pytest
import asyncio
from nats_pubsub import NATSClient

@pytest.mark.asyncio
async def test_nats_connection():
    client = NATSClient()
    await client.connect()
    assert client.nc is not None
    await client.close()

@pytest.mark.asyncio
async def test_handle_user_subscription():
    client = NATSClient()
    await client.connect()
    await client.handle_user_subscription("test_user", "test query")
    # Add assertions to check if the subscription was stored correctly
    await client.close()

@pytest.mark.asyncio
async def test_process_notification():
    client = NATSClient()
    await client.connect()
    await client.process_notification("Test notification")
    # Add assertions to check if the notification was processed correctly
    await client.close()
