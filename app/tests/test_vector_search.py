import pytest
from vector_search import store_embedding, search_similar_embeddings

@pytest.fixture
def sample_embedding():
    return [0.1] * 1536  # Assuming 1536-dimensional embeddings

def test_store_and_search_embedding(sample_embedding):
    metadata = {"user_id": "test_user", "query": "test query"}
    store_embedding(sample_embedding, metadata)
    
    results = search_similar_embeddings(sample_embedding, threshold=0.8)
    assert len(results) > 0
    assert results[0]["user_id"] == "test_user"
