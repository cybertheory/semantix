from config import Config
import weaviate

client = weaviate.Client(url=Config.WEAVIATE_URL)

def store_embedding(embedding, metadata):
    """
    Store the embedding and associated metadata in Weaviate.
    """
    data_object = {
        'metadata': metadata
    }
    client.batch.add_data_object(
        data_object=data_object,
        class_name='Subscription',
        vector=embedding
    )
    client.batch.flush()

def search_similar_embeddings(embedding, threshold):
    """
    Search for embeddings similar to the given embedding.
    """
    result = client.query.get(
        class_name='Subscription',
        properties=['metadata']
    ).with_near_vector({
        'vector': embedding,
        'certainty': threshold
    }).do()
    
    matching_subscriptions = []
    if 'data' in result and 'Get' in result['data']:
        subscriptions = result['data']['Get']['Subscription']
        for sub in subscriptions:
            metadata = sub['metadata']
            matching_subscriptions.append(metadata)
    return matching_subscriptions

# Ensure that the 'Subscription' class is created in Weaviate
def setup_weaviate_schema():
    if not client.schema.exists("Subscription"):
        class_obj = {
            "class": "Subscription",
            "properties": [
                {
                    "name": "metadata",
                    "dataType": ["text"]
                }
            ]
        }
        client.schema.create_class(class_obj)
    else:
        print("Subscription class already exists in Weaviate")

# Call the setup function at module load
setup_weaviate_schema()
