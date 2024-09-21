import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, Subscription, Webhook, User

@pytest.fixture(scope="module")
def test_db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()

def test_create_subscription(test_db):
    subscription = Subscription(user_id="test_user", query="test query")
    test_db.add(subscription)
    test_db.commit()
    assert test_db.query(Subscription).filter_by(user_id="test_user").first() is not None

def test_create_webhook(test_db):
    webhook = Webhook(url="http://test.com", is_active=True)
    test_db.add(webhook)
    test_db.commit()
    assert test_db.query(Webhook).filter_by(url="http://test.com").first() is not None

def test_create_user(test_db):
    user = User(username="testuser", hashed_password="hashedpassword")
    test_db.add(user)
    test_db.commit()
    assert test_db.query(User).filter_by(username="testuser").first() is not None
