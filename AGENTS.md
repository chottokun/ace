# ACEフレームワークを用いたRAGシステムの構築

## 0. 目的・背景

本プロジェクトの目的は、Agentic Context Engineering (ACE) フレームワークを活用し、高度な文脈理解能力を持つRAG（Retrieval-Augmented Generation）システムを構築することである。これにより、ユーザーの意図をより正確に汲み取り、精度の高い応答を生成するAIエージェントの開発を目指す。

## 1. はじめに

本ドキュメントは、現在実装されているAgentic Context Engineering (ACE) フレームワークの現状を評価し、`Docs/`でのドキュメント・サンプルコードを参考にACEを盛り込んだRAGシステムを構築するための指針を示す。

## 2. 実装について


### 2.1. 実装の見直し

- ACEフレームワークを利用したRAGシステムを構築するものである。
- 現在のレポジトリに含まれているのは不完全であり、全面的に見直す必要がある。`Docs/ace_lesson05.py`をベースにすべてみなおすこと。
- 特にACEフレームワークにおけるコンテキストの取り扱いについては、`Docs/ace_lesson05.py`を参考に断片化したコンテキストを構造化して取り扱うこと。

### 2.2. フロントエンド

- streamlitを用いた柔軟なUIを構築し、RAGの対話インターフェースを構築する。
- streamlitを用いたテストは、App testing https://docs.streamlit.io/develop/api-reference/app-testing を利用できる。

## 3. 環境構築について

### 3.1. セットアップ手順

`uv` を用いてPythonの仮想環境を構築し、パッケージを管理する。

1.  **仮想環境の作成**
    ```bash
    uv venv
    ```
2.  **仮想環境のアクティベート**
    ```bash
    # macOS / Linux
    source .venv/bin/activate
    # Windows
    .venv\Scripts\activate
    ```
3.  **依存関係のインストール**

依存関係は`pyproject.toml`に記述します：

```toml
[project.dependencies]
openai = "^1.3.5"
requests = "^2.31.0"
```
パッケージの追加

```bash
uv pip install <package-name>
uv pip add <package-name>  # pyproject.tomlに追記
```


### 3.2. 主要な依存パッケージ

以下は本プロジェクトで利用する主要なライブラリである。

- `streamlit`: フロントエンドUI
- `langchain`: LLMアプリケーションフレームワーク
- `transformers`: 自然言語処理ライブラリ
- `torch`: 機械学習フレームワーク
- （その他、必要に応じて追記）


