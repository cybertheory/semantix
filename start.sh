#!/bin/bash

# Wait for PostgreSQL to be ready
while ! nc -z db 5432; do
  sleep 0.1
done

# Initialize and start PostgreSQL
pg_ctl start

# Initialize and start NATS
nats-server &

# Initialize and start Weaviate
weaviate &

# Run database migrations
alembic upgrade head

# Start the FastAPI application
uvicorn main:app --host 0.0.0.0 --port 8000
