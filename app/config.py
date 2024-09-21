import os

class Config:
    # NATS configuration
    NATS_SERVER_URL = os.getenv('NATS_SERVER_URL', 'nats://localhost:4222')

    # Vector database configuration
    WEAVIATE_URL = os.getenv('WEAVIATE_URL', 'http://localhost:8080')

    # AI Model configuration
    USE_OPENAI = os.getenv('USE_OPENAI', 'True').lower() == 'true'
    USE_ANTHROPIC = os.getenv('USE_ANTHROPIC', 'False').lower() == 'true'
    USE_OLLAMA = os.getenv('USE_OLLAMA', 'False').lower() == 'true'

    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')

    # Anthropic Configuration
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '')

    # Ollama Configuration
    OLLAMA_SERVER_URL = os.getenv('OLLAMA_SERVER_URL', 'http://localhost:11434')
    OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'llama2')

    # Notification similarity threshold
    SIMILARITY_THRESHOLD = float(os.getenv('SIMILARITY_THRESHOLD', 0.8))

    # Notification settings (optional for email, Slack, etc.)
    NOTIFICATION_EMAIL = os.getenv('NOTIFICATION_EMAIL', 'false').lower() == 'true'
    NOTIFICATION_SLACK = os.getenv('NOTIFICATION_SLACK', 'false').lower() == 'true'

    # Database configuration
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost/semantix')
    ACCESS_TOKEN_EXPIRE_MINUTES = 30  # or any other value you prefer