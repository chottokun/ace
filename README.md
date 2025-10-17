# ACEフレームワークを活用したRAGシステムの単なるお試し

## 0. 参考文献
- 参考にさせていただきました。本レポジトリは論文内容を再現するものではありません。参考にして勉強のために自分なりに実装したものです。

**Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models**
- Qizheng Zhang, Changran Hu, Shubhangi Upasani, Boyuan Ma, Fenglu Hong, Vamsidhar Kamanuru, Jay Rainton, Chen Wu, Mengmeng Ji, Hanchen Li, Urmish Thakker, James Zou, Kunle Olukotun
- https://arxiv.org/html/2510.04618v1

## 1. 概要

本プロジェクトは、**Agentic Context Engineering (ACE) フレームワーク** の概念を基盤とし、**Retrieval-Augmented Generation (RAG)** を組み合わせた高度な対話AIシステムです。

ユーザーがアップロードしたPDFドキュメントの内容を外部知識として活用しつつ、対話を通じて得られるフィードバックからシステム自身が「教訓」を学習し、コンテキストを進化させます。これにより、より正確で文脈に適した回答を生成することを目指します。

フロントエンドには**Streamlit**を採用し、直感的なチャットUIとドキュメント管理機能を提供します。

## 2. 特徴

*   **ハイブリッドコンテキスト生成**:
    *   **外部コンテキスト**: ユーザーがアップロードしたPDFから、質問に関連する情報をリアルタイムで検索します。
    *   **進化的コンテキスト**: ACEフレームワークに基づき、過去の対話の成功・失敗から得られた教訓を蓄積・活用します。
*   **柔軟なバックエンド**:
    *   **LLM**: [Ollama](https://ollama.com/) を介して、ローカルで動作する様々なオープンソースLLM（例: `gemma3:4b`）を利用できます。
    *   **ベクトルデータベース**: [ChromaDB](https://www.trychroma.com/) を使用して、ドキュメントのベクトル情報を効率的に保存・検索します。
    *   **埋め込みモデル**: 日本語の扱いに優れた `cl-nagoya/ruri-v3-30m` を採用しています。
*   **インタラクティブなUI**:
    *   [Streamlit](https://streamlit.io/) による、リアルタイムでのチャット対話が可能です。
    *   複数のPDFファイルをドラッグ＆ドロップで簡単にアップロードできます。

## 3. アーキテクチャ

このシステムの主要なコンポーネントとデータフローは以下の通りです。

1.  **UI (Streamlit)**: ユーザーからのPDFファイルと質問を受け付けます。
2.  **Document Processor**: アップロードされたPDFを読み込み、テキストをチャンクに分割し、埋め込みモデルでベクトル化します。
3.  **Vector Store (ChromaDB)**: ベクトル化されたドキュメントチャンクを保存します。
4.  **Retriever**: ユーザーの質問に基づき、ChromaDBから関連性の高いドキュメントチャンクを検索します。
5.  **ACE Orchestrator**: ACEフレームワークの中核。以下の処理を統括します。
    *   **Context Store**から進化的コンテキストを取得します。
    *   **Retriever**から外部コンテキストを取得します。
    *   **Generator**に両方のコンテキストと質問を渡し、回答の草案（推論軌跡）を生成させます。
    *   **Reflector**が推論軌跡とフィードバック（現在はダミー）を分析し、新たな教訓（洞察）を抽出します。
    *   **Curator**が新たな教訓をContext Storeに統合し、コンテキストを進化させます。
6.  **LLM (Ollama)**: GeneratorやReflectorからの指示に基づき、テキスト生成を実行します。

## 4. セットアップと実行方法

### 4.1. 前提条件

*   Python 3.13 以上
*   [uv](https://github.com/astral-sh/uv): 高速なPythonパッケージ管理ツール
*   [Ollama](https://ollama.com/): ローカルでLLMを実行するためのプラットフォーム

### 4.2. インストール手順

1.  **OllamaとLLMのセットアップ**

    まず、Ollamaを公式サイトの指示に従ってインストールしてください。
    その後、ターミナルで以下のコマンドを実行し、本プロジェクトで使用するLLMをダウンロードします。

    ```bash
    ollama pull gemma3:4b
    ```

2.  **リポジトリのクローン**

    ```bash
    git clone <repository-url>
    cd ace
    ```

3.  **Python仮想環境の構築と依存関係のインストール**

    `uv` を使って、仮想環境の作成と必要なライブラリのインストールを一度に行います。

    ```bash
    # 仮想環境を作成
    uv venv

    # 仮想環境を有効化 (macOS / Linux)
    source .venv/bin/activate
    # (Windowsの場合: .venv\Scripts\activate)

    # 依存関係をインストール
    uv pip install -e .
    ```
    これにより、`pyproject.toml`に記載されたすべてのライブラリがインストールされます。

### 4.3. アプリケーションの起動

すべての準備が整ったら、以下のコマンドでStreamlitアプリケーションを起動します。

```bash
streamlit run main.py
```

コマンド実行後、ターミナルに表示されるURL（例: `http://localhost:8501`）をブラウザで開いてください。

## 5. 使い方

1.  **ドキュメントのアップロード**:
    *   画面左側のサイドバーにあるファイルアップローダーに、コンテキストとして使用したいPDFファイルをドラッグ＆ドロップします。
    *   「ドキュメントを処理」ボタンを押すと、ファイルのベクトル化とデータベースへの格納が始まります。

2.  **チャット**:
    *   ドキュメントの処理が完了したら、画面中央のチャット入力ボックスに質問を入力してください。
    *   AIは、アップロードされたPDFの内容と、自己学習した進化的コンテキストの両方を考慮して回答を生成します。

## 6. プロジェクト構成

```
/
├── ace_framework/         # ACEフレームワークのコアロジック
│   ├── context_store.py   # 進化的コンテキストの管理
│   ├── curator.py         # コンテキストの統合と整理
│   ├── document_processor.py # PDF処理とベクトル化
│   ├── generator.py       # 回答生成
│   ├── orchestrator.py    # ACEサイクル全体の統括
│   └── reflector.py       # 自己反省と洞察の抽出
├── chroma_db/             # ChromaDBの永続化データ
├── main.py                # Streamlitアプリケーションのエントリポイント
├── pyproject.toml         # プロジェクト設定と依存関係
└── README.md              # このファイル
```