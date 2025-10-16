# ace_framework/orchestrator.py

from .generator import Generator
from .reflector import Reflector
from .curator import Curator
from .context_store import ContextStore
from sentence_transformers import SentenceTransformer

class ACEOrchestrator:
    """
    目的： ジェネレーター、リフレクター、キュレーター間のフローを調整し、適応サイクルを管理します。
    """
    def __init__(self, generator: Generator, reflector: Reflector, curator: Curator, context_store: ContextStore, embedding_model: SentenceTransformer, retriever=None):
        self.generator = generator
        self.reflector = reflector
        self.curator = curator
        self.context_store = context_store
        self.embedding_model = embedding_model
        self.retriever = retriever

    def run_adaptation_cycle(self, query, feedback, mode, top_k=5):
        print(f"\n--- Running adaptation cycle in {mode} mode for query: {query} ---")
        
        # 1. 外部コンテキストを取得 (Retrieverが存在する場合)
        external_context_str = ""
        if self.retriever:
            print("Retrieving external context...")
            retrieved_docs = self.retriever.invoke(query)
            print(f"Retrieved {len(retrieved_docs)} documents from external source.")
            if retrieved_docs:
                print("--- Retrieved Documents ---")
                for i, doc in enumerate(retrieved_docs):
                    print(f"  Doc {i+1}: {doc.page_content[:200]}...") # Display first 200 chars
                print("-------------------------")
            external_context_str = "\n\n".join([doc.page_content for doc in retrieved_docs])
        else:
            print("No retriever available. Skipping external context retrieval.")

        # 2. 進化的コンテキストを取得
        evolutionary_context_items = self.context_store.retrieve_bullets(query=query, top_k=top_k, embedding_model=self.embedding_model)
        evolutionary_context_str = "\n".join([f"- {item['content']}" for item in evolutionary_context_items])

        # 3. 推論軌跡を生成
        trajectory, final_prompt = self.generator.generate_trajectory(evolutionary_context_str, external_context_str, query)

        # 4. 軌跡とフィードバックを反省
        reflection_output = self.reflector.reflect_on_trajectory(trajectory, feedback)
        insights = self.reflector.distill_insights(reflection_output)
        delta_entries = self.reflector.format_delta_entries(insights)

        # 5. コンテキストをキュレーション
        synthesized_delta = self.curator.synthesize_delta(delta_entries, evolutionary_context_items)
        merged_context = self.curator.merge_context(self.context_store.context, synthesized_delta)
        deduplicated_context = self.curator.perform_deduplication(merged_context)
        pruned_context = self.curator.prune_context(deduplicated_context)

        # 6. コンテキストストアを更新し、埋め込みを再生成
        self.context_store.context = pruned_context
        self.context_store.generate_and_store_embeddings(self.embedding_model)

        print("--- Adaptation cycle finished. ---")
        return trajectory, final_prompt, self.context_store.context

    def run_offline_adaptation(self, dataset, initial_context, epochs, top_k=5):
        print(f"\n--- Running offline adaptation for {epochs} epochs... ---")
        self.context_store.context = initial_context
        self.context_store.generate_and_store_embeddings(self.embedding_model)

        for epoch in range(epochs):
            print(f"\n--- Epoch {epoch + 1}/{epochs} ---")
            for data_point in dataset:
                query = data_point.get("query")
                feedback = data_point.get("feedback")
                if query and feedback is not None:
                    self.run_adaptation_cycle(query, feedback, mode="offline", top_k=top_k)
        return self.context_store.context

    def run_online_adaptation(self, stream_of_tasks, initial_context, top_k=5):
        print("\n--- Running online adaptation... ---")
        self.context_store.context = initial_context
        self.context_store.generate_and_store_embeddings(self.embedding_model)

        for task in stream_of_tasks:
            query = task.get("query")
            feedback = task.get("feedback")
            if query and feedback is not None:
                 self.run_adaptation_cycle(query, feedback, mode="online", top_k=top_k)
        return self.context_store.context
