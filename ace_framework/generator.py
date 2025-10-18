# ace_framework/generator.py

class Generator:
    """
    目的：現在の進化型コンテキストを使用して、推論軌跡を生成し、新しいタスクを解決しようとします。
    """
    def __init__(self, client, model_name):
        self.client = client
        self.model_name = model_name

    def generate_trajectory(self, evolutionary_context, external_context, query):
        print(f"Generating trajectory for query: '{query}'")
        prompt = f"""あなたはAIアシスタントです。以下の2種類のコンテキストを使用して、クエリを解決するための詳細な推論軌跡とクエリに対する回答を生成してください。応答は日本語で行ってください。

### クエリ
"{query}"

### 進化的コンテキスト (過去の対話からの教訓)
{evolutionary_context}

### 外部コンテキスト (ドキュメントからの情報)
{external_context}

### 指示
- ステップバイステップの推論軌跡とクエリに対する最終的な回答を生成してください。
"""
        print("\n--- Final Prompt Sent to LLM ---")
        print(prompt)
        print("----------------------------------\n")
        try:
            # Ollama chat APIを使用
            response = self.client.chat(
                model=self.model_name,
                messages=[
                    {
                        'role': 'user',
                        'content': prompt,
                    }
                ]
            )
            return response['message']['content'], prompt # chat APIの応答形式に対応
        except Exception as e:
            print(f"Error generating trajectory: {e}")
            return "推論軌跡の生成中にエラーが発生しました。", prompt
