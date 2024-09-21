import requests
from config import Config
import openai

def get_openai_embedding(text):
    """
    Generates an embedding for the input text using OpenAI's API.
    """
    openai.api_key = Config.OPENAI_API_KEY
    response = openai.embeddings.create(
        input=text,
        model='text-embedding-3-large'
    )
    return response['data'][0]['embedding']

def get_anthropic_embedding(text):
    """
    Placeholder function for generating embeddings using Anthropic's API.
    As of now, Anthropic's API does not provide a direct method for generating embeddings.
    You may need to use an alternative method or a different service for embeddings.
    """
    raise NotImplementedError("Anthropic embedding generation is not currently supported.")

def get_ollama_embedding(text):
    """
    Generates an embedding for the input text using Ollama.
    Assumes that an Ollama server is running and accessible.
    """
    url = f"{Config.OLLAMA_SERVER_URL}/api/embeddings"
    payload = {
        "model": Config.OLLAMA_MODEL,
        "text": text
    }
    headers = {
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()
        return result.get('embedding')
    except requests.exceptions.RequestException as e:
        raise Exception(f"Ollama embedding API call failed: {e}")

def get_embedding(text):
    """
    Determines which embedding function to use based on configuration.
    """
    if Config.USE_OPENAI:
        return get_openai_embedding(text)
    elif Config.USE_ANTHROPIC:
        return get_anthropic_embedding(text)
    elif Config.USE_OLLAMA:
        return get_ollama_embedding(text)
    else:
        raise Exception("No valid model selected for generating embeddings.")

