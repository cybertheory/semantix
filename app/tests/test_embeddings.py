import pytest
from embeddings import get_embedding, get_openai_embedding, get_ollama_embedding
from config import Config

def test_get_embedding():
    Config.USE_OPENAI = True
    embedding = get_embedding("Test query")
    assert isinstance(embedding, list)
    assert len(embedding) > 0

@pytest.mark.skipif(not Config.OPENAI_API_KEY, reason="OpenAI API key not set")
def test_get_openai_embedding():
    embedding = get_openai_embedding("Test query")
    assert isinstance(embedding, list)
    assert len(embedding) > 0

@pytest.mark.skipif(not Config.USE_OLLAMA, reason="Ollama not enabled")
def test_get_ollama_embedding():
    embedding = get_ollama_embedding("Test query")
    assert isinstance(embedding, list)
    assert len(embedding) > 0
