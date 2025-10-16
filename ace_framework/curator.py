# ace_framework/curator.py

class Curator:
    """
    目的：リフレクターの洞察をメインコンテキストに統合し、その構造を維持し、冗長性を防ぎます。
    """
    def __init__(self, client=None, model_name=None):
        self.client = client
        self.model_name = model_name

    def synthesize_delta(self, delta_entries, existing_context):
        print(f"Synthesizing delta from {len(delta_entries)} entries...")
        # 本格的な実装では、ここでデルタを既存コンテキストと照合・合成
        return delta_entries

    def merge_context(self, existing_context, delta_entries):
        print("Merging context...")
        new_context = existing_context.copy()
        existing_content = {item['content'] for item in existing_context}
        for entry in delta_entries:
            if entry['content'] not in existing_content:
                new_context.append(entry)
                existing_content.add(entry['content'])
        return new_context

    def perform_deduplication(self, context):
        print("Performing deduplication...")
        # 本格的な実装では、埋め込みの類似度に基づいて重複を削除します
        # 現在は簡易的にcontentの重複を削除
        seen = set()
        deduplicated = []
        for item in context:
            if item['content'] not in seen:
                deduplicated.append(item)
                seen.add(item['content'])
        return deduplicated

    def prune_context(self, context):
        print("Pruning context...")
        # 本格的な実装では、関連性や使用頻度に基づいて項目を削除します
        # 現在は簡易的に項目数を制限しない
        return context
