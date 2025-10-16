# ace_framework/reflector.py

from pydantic import BaseModel, Field
from typing import List

# Pydanticモデルの定義：抽出する洞察の構造
class Insight(BaseModel):
    content: str = Field(..., description="再利用可能な教訓または観察事項")

class InsightsList(BaseModel):
    insights: List[Insight] = Field(..., description="抽出された洞察のリスト")

class Reflector:
    """
    目的：ジェネレーターのパフォーマンスを批判的に分析し、実行可能な洞察を抽出します。
    """
    def __init__(self, client, model_name):
        self.client = client
        self.model_name = model_name

    def reflect_on_trajectory(self, trajectory, feedback):
        print(f"Reflecting on trajectory with feedback: '{feedback}'")
        prompt = f"""以下の推論軌跡とフィードバックを分析してください。批判的な反省を提供してください。応答は日本語で行ってください。
推論軌跡:
{trajectory}

フィードバック:
{feedback}

何がうまくいったか、何がうまくいかなかったか、そしてその理由を特定してください。
"""
        print("\n--- Reflection Prompt Sent to LLM ---")
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
            return response['message']['content'] # chat APIの応答形式に対応
        except Exception as e:
            print(f"Error reflecting on trajectory: {e}")
            return "推論軌跡の反省中にエラーが発生しました。"

    def distill_insights(self, reflection_output):
        print(f"Distilling insights from reflection into structured format...")
        prompt = f"""以下の反省結果から、具体的で再利用可能な教訓または洞察を抽出してください。出力は提供されたJSONスキーマに厳密に従ったJSONオブジェクト形式で行ってください。応答内容は日本語で記述してください。
反省結果:
{reflection_output}

このJSONスキーマに厳密に従ってください:
{InsightsList.model_json_schema()}
"""
        print("\n--- Distillation Prompt Sent to LLM ---")
        print(prompt)
        print("----------------------------------\n")
        try:
            # Ollama chat APIと構造化出力を使用
            response = self.client.chat(
                model=self.model_name,
                messages=[
                    {
                        'role': 'user',
                        'content': prompt,
                    }
                ],
                format='json' # JSON形式での出力を要求
            )
            # JSON応答をパースしてPydanticモデルに検証
            insights_data = response['message']['content']
            insights_list_obj = InsightsList.model_validate_json(insights_data)
            # Pydanticオブジェクトから洞察のリスト（文字列）を抽出
            insights = [item.content for item in insights_list_obj.insights]
            return insights
        except Exception as e:
            print(f"Error distilling insights: {e}")
            print(f"Raw response content: {response.get('message', {}).get('content', 'N/A')}")
            return ["洞察の抽出中にエラーが発生しました。"]

    def format_delta_entries(self, insights):
        print("Formatting insights into delta entries...")
        # 抽出された洞察は既に意味のある単位になっていると仮定し、そのままdelta entryに変換
        return [{"content": i, "metadata": {}} for i in insights]
