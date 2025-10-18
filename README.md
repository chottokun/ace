# ACEフレームワークに基づく自己進化型RAGシステムの検討（試行錯誤）

## 0. 参考文献

本プロジェクトは、以下の論文で提唱された概念に強くインスパイアされています。論文内容の完全な再現を目的とするものではなく、そのアイデアを基に学習目的で独自に実装したものです。

**Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models**
- Qizheng Zhang, Changran Hu, Shubhangi Upasani, Boyuan Ma, Fenglu Hong, Vamsidhar Kamanuru, Jay Rainton, Chen Wu, Mengmeng Ji, Hanchen Li, Urmish Thakker, James Zou, Kunle Olukotun
- https://arxiv.org/html/2510.04618v1

## 1. 概要

このプロジェクトは、**Agentic Context Engineering (ACE) フレームワーク**と**Retrieval-Augmented Generation (RAG)**を組み合わせた、高度な対話AIシステムです。

ユーザーがアップロードしたPDFドキュメントを外部知識として活用しつつ、対話からのフィードバックを通じてシステムが自律的に「教訓」を学習し、コンテキストを進化させます。これにより、時間と共により正確で文脈に適した回答を生成する能力の獲得を目指します。

ユーザーインターフェースには**Streamlit**を採用し、直感的なチャットUIとドキュメント管理機能を提供します。

## 2. 主な特徴

*   **ハイブリッドコンテキスト生成**:
    *   **外部コンテキスト (RAG)**: ユーザーがアップロードしたPDFから、質問に最も関連する情報をリアルタイムで検索・抽出します。
    *   **進化的コンテキスト (ACE)**: 過去の対話の成功・失敗から得られた「教訓」を蓄積し、回答生成時に活用します。
*   **柔軟なバックエンド**:
    *   **LLM**: [Ollama](https://ollama.com/) を介して、`gemma3:4b` などの様々なオープンソースLLMをローカル環境で利用可能です。
    *   **ベクトルデータベース**: [ChromaDB](https://www.trychroma.com/) を使用し、ドキュメントのベクトル情報を効率的に保存・検索します。
    *   **埋め込みモデル**: 日本語の扱いに優れた `cl-nagoya/ruri-v3-30m` を採用しています。
*   **インタラクティブなUI**:
    *   [Streamlit](https://streamlit.io/) により、リアルタイムでのチャット対話を実現します。
    *   複数のPDFファイルをドラッグ＆ドロップで簡単にアップロードできます。

## 3. アーキテクチャ

システムの主要コンポーネントとデータフローは以下の通りです。

1.  **UI (Streamlit)**: ユーザーからのPDFファイルアップロードと質問入力を受け付けます。
2.  **Document Processor**: アップロードされたPDFを読み込み、テキストをチャンク（断片）に分割後、埋め込みモデルでベクトル化します。
3.  **Vector Store (ChromaDB)**: ベクトル化されたドキュメントチャンクを永続化します。
4.  **Retriever**: ユーザーの質問に基づき、ChromaDBから関連性の高いドキュメントチャンクを検索します。
5.  **ACE Orchestrator**: ACEフレームワークの中核を担い、以下のプロセスを統括します。
    *   **Context Store**から進化的コンテキストを取得。
    *   **Retriever**から外部コンテキストを取得。
    *   **Generator**に両コンテキストと質問を渡し、回答の草案（推論軌跡）を生成させる。
    *   **Reflector**が推論軌跡とフィードバックを分析し、新たな教訓（洞察）を抽出する。
    *   **Curator**が新たな教訓をContext Storeに統合し、コンテキストを進化させる。
6.  **LLM (Ollama)**: GeneratorやReflectorからの要求に基づき、テキスト生成タスクを実行します。

## 4. セットアップと実行

### 4.1. 前提条件

*   Python 3.13 以降
*   [uv](https://github.com/astral-sh/uv): 高速なPythonパッケージインストーラー
*   [Ollama](https://ollama.com/): LLMをローカルで実行するためのプラットフォーム

### 4.2. インストール

1.  **OllamaとLLMのセットアップ**

    公式サイトの指示に従いOllamaをインストール後、ターミナルで以下のコマンドを実行して、本プロジェクトで使用するLLMをダウンロードします。

    ```bash
    ollama pull gemma3:4b
    ```

2.  **リポジトリのクローン**

    ```bash
    git clone {}
    cd ace
    ```

3.  **Python仮想環境の構築と依存関係のインストール**

    `uv` を使用して、仮想環境の作成とライブラリのインストールを効率的に行います。

    ```bash
    # 仮想環境を作成
    uv venv

    # 仮想環境を有効化 (macOS / Linux)
    source .venv/bin/activate
    # (Windowsの場合: .venv\Scripts\activate)

    # 依存関係をインストール
    uv pip install -e .
    ```
    これにより、`pyproject.toml`に定義されたすべての依存関係がインストールされます。

### 4.3. アプリケーションの起動

以下のコマンドでStreamlitアプリケーションを起動します。

```bash
streamlit run main.py
```

ターミナルに表示されるURL（例: `http://localhost:8501`）をブラウザで開いてください。

## 5. 使用方法

1.  **ドキュメントのアップロード**:
    *   画面左側のサイドバーにあるアップローダーに、知識源としたいPDFファイルをドラッグ＆ドロップします。
    *   「ドキュメントを処理」ボタンを押すと、ファイルの解析、ベクトル化、データベースへの格納が実行されます。
2.  **チャット**:
    *   ドキュメントの処理が完了したら、中央のチャット入力ボックスに質問を入力します。
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