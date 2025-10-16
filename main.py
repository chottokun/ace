# main.py
import streamlit as st
from ollama import Client
from sentence_transformers import SentenceTransformer

from ace_framework.context_store import ContextStore
from ace_framework.generator import Generator
from ace_framework.reflector import Reflector
from ace_framework.curator import Curator
from ace_framework.orchestrator import ACEOrchestrator
from ace_framework.document_processor import process_uploaded_files

st.set_page_config(layout="wide")
st.title("ACE Framework RAG System")

# --- 初期化 ---
@st.cache_resource
def load_models_and_clients():
    """
    モデルとクライアントをロードし、キャッシュする。
    """
    print("Loading models and clients...")
    try:
        embedding_model = SentenceTransformer('cl-nagoya/ruri-v3-30m')
        ollama_client = Client()
        ollama_client.list()
        print("Models and clients loaded successfully.")
        return embedding_model, ollama_client
    except Exception as e:
        st.error(f"モデルまたはOllamaクライアントのロード中にエラーが発生しました: {e}")
        st.info("Ollamaがローカルで実行されていることを確認してください。")
        return None, None

embedding_model, ollama_client = load_models_and_clients()

# --- session_stateの初期化 ---
if 'ace_initialized' not in st.session_state:
    st.session_state.ace_initialized = False
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'retriever' not in st.session_state:
    st.session_state.retriever = None


# --- サイドバー (ファイルアップロード) ---
with st.sidebar:
    st.header("ドキュメント設定")
    uploaded_files = st.file_uploader(
        "コンテキストとして使用するPDFファイルをアップロードしてください",
        type="pdf",
        accept_multiple_files=True
    )
    if st.button("ドキュメントを処理"):
        if uploaded_files and embedding_model:
            with st.spinner("ドキュメントを処理中..."):
                st.session_state.retriever = process_uploaded_files(
                    uploaded_files,
                    embedding_model,
                    collection_name="rag_collection"
                )
                if st.session_state.retriever:
                    st.success("ドキュメントの処理が完了しました。")
                else:
                    st.error("ドキュメントの処理に失敗しました。")
        elif not uploaded_files:
            st.warning("ファイルをアップロードしてください。")

    st.subheader("現在の進化的コンテキスト")
    if 'context_store' in st.session_state and st.session_state.context_store.context:
        context_contents = [item.get('content', 'N/A') for item in st.session_state.context_store.context]
        st.json(context_contents)
    else:
        st.info("まだコンテキストはありません。")


# --- メインコンテンツ (チャット) ---
if embedding_model and ollama_client:
    # ACEコンポーネントの初期化（初回のみ）
    if not st.session_state.ace_initialized:
        print("Initializing ACE components...")
        MODEL_NAME = "gemma3:4b"
        
        context_store = ContextStore()
        context_store.add_bullet("メモ化の良い戦略は、辞書を使って結果を保存することです。")
        context_store.generate_and_store_embeddings(embedding_model)
        
        st.session_state.context_store = context_store
        st.session_state.generator = Generator(ollama_client, MODEL_NAME)
        st.session_state.reflector = Reflector(ollama_client, MODEL_NAME)
        st.session_state.curator = Curator(ollama_client, MODEL_NAME)
        st.session_state.ace_initialized = True
        print("ACE components initialized.")

    # OrchestratorはRetrieverの状態によって動的に再生成
    orchestrator = ACEOrchestrator(
        st.session_state.generator,
        st.session_state.reflector,
        st.session_state.curator,
        st.session_state.context_store,
        embedding_model,
        retriever=st.session_state.retriever
    )

    st.subheader("対話")

    # チャット履歴の表示
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # ユーザー入力
    query = st.chat_input("質問を入力してください")

    if query:
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)

        with st.spinner("思考中..."):
            feedback = " " # UIからフィードバックを得る方法は後で考える
            
            trajectory, final_prompt, updated_context = orchestrator.run_adaptation_cycle(
                query=query,
                feedback=feedback,
                mode="online",
                top_k=5
            )
            response = trajectory

        # AIメッセージを履歴に追加して表示
        formatted_response = f"回答：\n\n{response}"
        st.session_state.messages.append({"role": "assistant", "content": formatted_response})
        with st.chat_message("assistant"):
            st.markdown(formatted_response)
            with st.expander("最適化されたプロンプトを表示"):
                st.text(final_prompt)

else:
    st.warning("ACEコンポーネントを初期化できませんでした。Ollamaが起動しているか確認してください。")
