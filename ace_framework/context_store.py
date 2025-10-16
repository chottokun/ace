# ace_framework/context_store.py

import torch
from sentence_transformers import SentenceTransformer

class ContextStore:
    """
    目的： 進化型コンテキストを構成する「項目」のコレクションを管理します。
    """
    def __init__(self):
        self.context = []

    def add_bullet(self, bullet_content, embedding=None, metadata=None):
        if metadata is None: metadata = {}
        bullet = {"content": bullet_content, "embedding": embedding, "metadata": metadata}
        print(f"Adding bullet: {bullet['content']}")
        self.context.append(bullet)

    def retrieve_bullets(self, query, top_k, embedding_model):
        print(f"Retrieving top {top_k} bullets for query: '{query}'")
        if not self.context or query is None:
            return []

        query_embedding = embedding_model.encode(query, convert_to_tensor=True)
        # Move item embeddings to the same device as the query embedding
        item_embeddings = torch.stack([torch.tensor(item["embedding"]).to(query_embedding.device) for item in self.context if item.get("embedding") is not None])

        if item_embeddings.nelement() == 0: # Check if tensor is empty
            return []

        # コサイン類似度を計算
        cos_scores = torch.nn.functional.cosine_similarity(query_embedding, item_embeddings)
        top_results = torch.topk(cos_scores, k=min(top_k, len(self.context)))

        return [self.context[i] for i in top_results.indices]

    def generate_and_store_embeddings(self, embedding_model):
        print("Generating and storing embeddings for context items...")
        for item in self.context:
            if item.get("content") and item.get("embedding") is None:
                item["embedding"] = embedding_model.encode(item["content"]).tolist() # Store as list for easier serialization
        print("Finished generating and storing embeddings.")
