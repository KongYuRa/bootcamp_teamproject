import os
import openai
import warnings
from langchain_openai import OpenAIEmbeddings
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma

openai.api_key = os.environ.get("MY_OPENAI_API_KEY")
# EMBED = OllamaEmbeddings(model="nomic-embed-text")
EMBED = OpenAIEmbeddings(model="text-embedding-ada-002", api_key=openai.api_key)


def create_vstore(DOCS, DB_NAME: str, DB_PATH):
    """
    크로마 db 생성

    Parameters:
        DOCS : 포함할 문서 ; documents 객체
        DB_NAME : db 생성시 설정한 이름
        DB_PATH : db 경로
    Returns:
        Chroma 객체
    """
    return Chroma.from_documents(
        documents=DOCS,
        collection_name=DB_NAME,
        persist_directory=DB_PATH,
        embedding=EMBED,
    )


def load_vstore(DB_NAME: str, DB_PATH):
    """
    로컬에 저장된 크로마 db를 불러옴

    Parameters:
        DB_NAME : db 생성시 설정한 이름
        DB_PATH : db 경로
    Returns:
        Chroma 객체
    """
    return Chroma(
        collection_name=DB_NAME,
        persist_directory=DB_PATH,
        embedding_function=EMBED,
    )


def add_to_vstore(SCRIPT, DB):
    """
    새로 생성된 스크립트를 documets 객체로 변경 후 db에 저장

    Parameters:
        SCRIPT : 추가할 스크립트  ; documents 객체
        DB : 저장할 db
    Returns:
        Chroma db에 데이터 추가
    """
    script_documents = [
        Document(page_content=SCRIPT),
    ]
    DB.add_documents(script_documents)
    DB.persist()
