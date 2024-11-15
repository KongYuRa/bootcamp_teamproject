# 1. 사용환경 준비 (OpenAI 모델)

import os

from dotenv import load_dotenv


load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


# 2. 모델 로드하기

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# 모델 초기화
model = ChatOpenAI(model="gpt-4o-mini")



# 3. 문서 로드하기 (인공지능산업최신동향_2024년11월호.pdf)
# from langchain.document_loaders import PyPDFLoader

from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("/Users/ur/Desktop/Git/project/인공지능산업최신동향_2024년11월호.pdf")

#loader = PyPDFLoader("/Users/ur/Desktop/Git/project/초거대 언어모델 연구 동향 (1).pdf")
#loader = PyPDFLoader("/Users/ur/Desktop/Git/project/[2024 한권으로 OK 주식과 세금].pdf")


# 페이지 별 문서 로드
docs = loader.load()



# 4. 문서 청크로 나누기

# 4-1. CharacterTextSplitter
from langchain.text_splitter import CharacterTextSplitter

text_splitter = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=100,
    chunk_overlap=10,
    length_function=len,
    is_separator_regex=False,
)

splits = text_splitter.split_documents(docs)


# 4-2. RecursiveCharacterTextSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter

recursive_text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=10,
    length_function=len,
    is_separator_regex=False,
)

splits = recursive_text_splitter.split_documents(docs)

print(splits)