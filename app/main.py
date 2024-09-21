import asyncio
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import init_db, get_db, Webhook, User
from pydantic import BaseModel
import uvicorn
from nats_pubsub import NATSClient
from config import Config
from logger import app_logger
from auth import authenticate_user, create_access_token, get_current_user, get_password_hash
from datetime import timedelta
from config import Config
# Initialize FastAPI app
app = FastAPI()


ACCESS_TOKEN_EXPIRE_MINUTES = Config.ACCESS_TOKEN_EXPIRE_MINUTES


# Create an instance of NATSClient
nats_client = NATSClient()

@app.on_event("startup")
async def startup_event():
    init_db()
    await nats_client.connect()
    app_logger.info("Semantix system is running. Waiting for user subscriptions and notifications...")

@app.on_event("shutdown")
async def shutdown_event():
    # Close NATS connection when the app shuts down
    await nats_client.close()

@app.post("/subscribe/")
async def subscribe(user_id: str, user_query: str):
    await nats_client.handle_user_subscription(user_id, user_query)
    app_logger.info(f"User '{user_id}' subscribed with query '{user_query}'")
    return {"message": f"User '{user_id}' subscribed with query '{user_query}'"}

@app.post("/publish/")
async def publish(notification_text: str):
    await nats_client.process_notification(notification_text)
    app_logger.info(f"Notification processed: {notification_text[:50]}...")
    return {"message": "Notification processed"}

class WebhookCreate(BaseModel):
    url: str
    metadata: dict = None

@app.post("/webhooks/")
async def create_webhook(webhook: WebhookCreate, db: Session = Depends(get_db)):
    db_webhook = Webhook(url=webhook.url, metadata=webhook.metadata)
    db.add(db_webhook)
    db.commit()
    db.refresh(db_webhook)
    return db_webhook

@app.get("/webhooks/")
async def list_webhooks(db: Session = Depends(get_db)):
    return db.query(Webhook).all()

@app.delete("/webhooks/{webhook_id}")
async def delete_webhook(webhook_id: int, db: Session = Depends(get_db)):
    webhook = db.query(Webhook).filter(Webhook.id == webhook_id).first()
    if not webhook:
        raise HTTPException(status_code=404, detail="Webhook not found")
    db.delete(webhook)
    db.commit()
    return {"message": "Webhook deleted successfully"}

@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/setup")
async def first_time_setup(username: str, password: str, db: Session = Depends(get_db)):
    if db.query(User).first():
        raise HTTPException(status_code=400, detail="Setup has already been completed")
    hashed_password = get_password_hash(password)
    new_user = User(username=username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    return {"message": "First-time setup completed successfully"}

@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

if __name__ == "__main__":
    # Run the FastAPI app using Uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
