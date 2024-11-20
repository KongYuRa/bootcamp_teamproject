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
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("/Users/ur/Desktop/Git/project/인공지능산업최신동향_2024년11월호.pdf")

loader = PyPDFLoader("/Users/ur/Desktop/Git/project/초거대 언어모델 연구 동향 (1).pdf")
loader = PyPDFLoader("/Users/ur/Desktop/Git/project/[2024 한권으로 OK 주식과 세금].pdf")


# 페이지 별 문서 로드
docs = loader.load()

#print(docs)


# 4. 문서 청크로 나누기 (사용X)
# # 4-1. CharacterTextSplitter
# from langchain.text_splitter import CharacterTextSplitter # 문서를 개별 문자 단위로 나누기

# text_splitter = CharacterTextSplitter(  # 주어진 텍스트를 문자 단위로 분할
#     separator="\n\n",           # 분할된 각 청크를 구분할 때 기준이 되는 문자열
#     chunk_size=100,             # 각 청크의 최대 길이(최대 100자)
#     chunk_overlap=10,           # 인접한 청크 사이에 중복으로 포함될 문자의 수 (100자 중복)
#     length_function=len,        # 청크의 길이 계산 (문자열의 길이 기반)
#     is_separator_regex=False,   # 구분자로 정규식을 사용하지 않음 (문자열 데이터 중에서 원하는 조건(패턴)과 일치하는 문자열 부분을 찾아내기 위해 미리 정의된 기호와 문자를 사용하여 작성한 문자열)
# )

# splits = text_splitter.split_documents(docs)    # 문서 파일을 load한 후 다시 작은 단위조각의 List[Document] 로 반환



# 4-2. RecursiveCharacterTextSplitter (시용)
from langchain.text_splitter import RecursiveCharacterTextSplitter  #텍스트를 재귀적으로 분할 (자신을 재사용하여 정의)

recursive_text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,             # 각 청크의 최대 길이(최대 100자)
    chunk_overlap=10,           # 인접한 청크 사이에 중복으로 포함될 문자의 수 (100자 중복)
    length_function=len,        # 청크의 길이 계산 (문자열의 길이 기반)  
    is_separator_regex=False,   # 구분자로 정규식을 사용하지 않음 (문자열 데이터 중에서 원하는 조건(패턴)과 일치하는 문자열 부분을 찾아내기 위해 미리 정의된 기호와 문자를 사용하여 작성한 문자열)
)

splits = recursive_text_splitter.split_documents(docs)    # 문서 파일을 load한 후 다시 작은 단위조각의 List[Document] 로 반환

#print(splits)



# 5. 벡터 임베딩 생성
from langchain_openai import OpenAIEmbeddings

# OpenAI 임베딩 모델 초기화
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")



# 6. 벡터 스토어 생성
from langchain_community.vectorstores import FAISS

vectorstore = FAISS.from_documents(documents=splits, embedding=embeddings)



# 7. FAISS를 Retriever로 변환
from langchain.vectorstores.base import VectorStore

#retriever = VectorStore.as_retriever(search_type="similarity", search_kwargs={"k": 1})
retriever = vectorstore.as_retriever()



# 8. 프롬프트 템플릿 정의 
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

# 프롬프트 템플릿 정의
contextual_prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer the question using only the following context."),
    ("user", "Context: {context}\\n\\nQuestion: {question}")
])



# 9. RAG 체인 구성
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

# 프롬프트 템플릿 정의
contextual_prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer the question using only the following context."),
    ("user", "Context: {context}\\n\\nQuestion: {question}")
])

class DebugPassThrough(RunnablePassthrough):
    def invoke(self, *args, **kwargs):
        output = super().invoke(*args, **kwargs)
        print("Debug Output:", output)
        return output
    
# 문서 리스트를 텍스트로 변환하는 단계 추가
class ContextToText(RunnablePassthrough):
    def invoke(self, inputs, config=None, **kwargs):  # config 인수 추가
        # context의 각 문서를 문자열로 결합
        context_text = "\n".join([doc.page_content for doc in inputs["context"]])
        return {"context": context_text, "question": inputs["question"]}

# RAG 체인에서 각 단계마다 DebugPassThrough 추가
rag_chain_debug = {
    "context": retriever,                    # 컨텍스트를 가져오는 retriever
    "question": DebugPassThrough()        # 사용자 질문이 그대로 전달되는지 확인하는 passthrough
}  | DebugPassThrough() | ContextToText()|   contextual_prompt | model



# 10. 챗봇 구동 확인
while True:
	print("========================")
	query = input("질문을 입력하세요: ")
	response = rag_chain_debug.invoke(query)
	print("Final Response:")
	print(response.content)



# 질문을 했을 때 pdf의 자료를 취합하여 답변을 주게 되는데, 한정되어 있기 때문에 답이 명확하지 않을 수 있습니다.
# RAG 기술을 사용한다면 최신 자료들을 제공해줄 수 있고, 정확한 자료를 주기 때문에 양질의 답을 얻을 수 있습니다.(더 구체적인 답)

