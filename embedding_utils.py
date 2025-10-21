import cohere

def get_cohere_embeddings(text, api_key):
    co = cohere.Client(api_key)
    if isinstance(text, str):
        text = [text]
    resp = co.embed(model="embed-english-v2.0", texts=text)
    return resp.embeddings[0]
