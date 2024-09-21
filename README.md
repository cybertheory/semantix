# Semantix

Semantix is a powerful semantic notification system that leverages AI and vector databases for intelligent subscription handling and notification processing.

## Features

- Intelligent subscription handling using natural language queries
- Advanced notification processing with semantic similarity matching
- Multi-model AI integration (OpenAI, Anthropic, Ollama)
- Scalable architecture using NATS for pub/sub messaging
- Vector database integration with Weaviate
- PostgreSQL for persistent storage
- Configurable webhooks for external system integration
- RESTful API built with FastAPI
- Robust authentication using JWT
- Comprehensive logging system
- Containerized deployment with Docker

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Installation

1. Clone the repository:
git clone https://github.com/yourusername/semantix.git cd semantix
2. Build and start the containers:
docker-compose up --build
3. The API will be available at `http://localhost:8000`

### First-time Setup

Create the first admin user:

```curl -X POST "http://localhost:8000/setup?username=admin&password=adminpassword"```


### Authentication

Obtain an access token:

```curl -X POST http://localhost:8000/token
-H "Content-Type: application/x-www-form-urlencoded"
-d "username=admin&password=adminpassword"```


### Creating a Subscription
```curl -X POST "http://localhost:8000/subscribe/?user_id=testuser&user_query=AI%20and%20machine%20learning%20updates"
-H "Authorization: Bearer YOUR_ACCESS_TOKEN"```


## Configuration

Environment variables can be set in the docker-compose.yml file or through the CLI:

```OPENAI_API_KEY=your_api_key USE_OPENAI=True SIMILARITY_THRESHOLD=0.8 docker-compose up```


## Testing

Run the test suite:
docker-compose exec app pytest tests/


## Contributing

Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.