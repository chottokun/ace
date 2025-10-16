# ace_framework/document_processor.py
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from sentence_transformers import SentenceTransformer
from typing import List
import os

def process_uploaded_files(uploaded_files: List, embedding_model: SentenceTransformer, collection_name: str = "rag_collection"):
    """
    アップロードされたPDFファイルを処理し、ChromaDBに格納してRetrieverを返す。
    """
    if not uploaded_files:
        return None

    # アップロードされたファイルを一時的に保存
    temp_dir = "temp_docs"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    docs = []
    for uploaded_file in uploaded_files:
        temp_path = os.path.join(temp_dir, uploaded_file.name)
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # PyPDFLoaderを使用してドキュメントをロード
        loader = PyPDFLoader(temp_path)
        docs.extend(loader.load())

    # テキストをチャンクに分割
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    if not splits:
        st.warning("ドキュメントからテキストを抽出できませんでした。")
        return None

    # ChromaDBにドキュメントを格納
    # LangChainのChroma統合はSentenceTransformerモデルを直接受け取れないため、
    # SentenceTransformerEmbeddingFunctionというラッパーを使うか、HuggingFaceEmbeddingsを使う必要がある。
    # ここではシンプルにするため、LangChainが推奨するHuggingFaceEmbeddingsを使用する。
    # sentence-transformersライブラリはHuggingFaceのモデルをダウンロードするために内部で使用される。
    from langchain_community.embeddings import HuggingFaceEmbeddings

    # SentenceTransformerモデル名を指定してHuggingFaceEmbeddingsを初期化
    embeddings = HuggingFaceEmbeddings(model_name='cl-nagoya/ruri-v3-30m')

    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        collection_name=collection_name,
        persist_directory="./chroma_db" # データを永続化
    )

    st.success(f"{len(splits)}個のドキュメントチャンクをChromaDBに格納しました。")

    return vectorstore.as_retriever()
