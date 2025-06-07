import requests

class Embeddings:
    def embed_documents(self, texts):
        response = requests.post(
            "https://asteroide.ing.uc.cl/api/embed",
            json={
                "model": "nomic-embed-text",
                "input": texts
            }
        )
        response.raise_for_status()
        return response.json()["embeddings"]

    def embed_query(self, text):
        return self.embed_documents([text])[0]
