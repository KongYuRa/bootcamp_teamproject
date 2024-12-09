import os
import json
import openai
from openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain.memory import ConversationSummaryMemory
from langchain_core.output_parsers import StrOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter

openai.api_key = os.environ.get("MY_OPENAI_API_KEY")


def process_json_data(json_files):
    """
    여러 JSON 파일을 읽고 데이터를 통합한 후 특정 형식의 문자열 리스트로 반환

    Parameters:
        json_files (list): JSON 파일 경로 리스트

    Returns:
        list: 파일 데이터에서 'title'과 'content'를 읽어 특정 형식으로 변환한 리스트
    """
    all_json_data = []
    for file_path in json_files:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                all_json_data.extend(data)
        except FileNotFoundError:
            print(f"Error: 파일을 찾을 수 없습니다 - {file_path}")
        except json.JSONDecodeError:
            print(f"Error: JSON 파일 형식이 잘못되었습니다 - {file_path}")

    # 'title'과 'content'를 읽어 특정 형식으로 반환
    return [
        f"Title: {item.get('title', 'N/A')}\nContent: {item.get('content', 'N/A')}"
        for item in all_json_data
    ]


def title_json_data(json_files):
    """
    여러 JSON 파일을 읽고 데이터를 통합한 후 특정 형식의 문자열 리스트로 반환

    Parameters:
        json_files (list): JSON 파일 경로 리스트

    Returns:
        list: 파일 데이터에서 'title'을 읽어 특정 형식으로 변환한 리스트
    """
    all_json_data = []
    for file_path in json_files:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                all_json_data.extend(data)
        except FileNotFoundError:
            print(f"Error: 파일을 찾을 수 없습니다 - {file_path}")
        except json.JSONDecodeError:
            print(f"Error: JSON 파일 형식이 잘못되었습니다 - {file_path}")

    # 'title'과 'content'를 읽어 특정 형식으로 반환
    title = [item.get("title", "N/A") for item in all_json_data]
    return title


def split_texts(texts, chunk_size=1000, chunk_overlap=200):
    """
    텍스트 데이터를 입력 받아 분할

    Parameters:
        texts: 텍스트 데이터

    Returns:
        Document 객체
    """
    recursive_text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        is_separator_regex=False,
    )
    documents = [Document(page_content=texts)]
    return recursive_text_splitter.split_documents(documents)


def documents_filter(SPLITS):
    """
    분할된 데이터에서 불필요한 데이터를 제거하고 하나로 결합
    ConversationSummaryMemory에 이전 내용을 요약하여 저장
    아전 내용과 대조해서 불필요한 데이터 구분

    Parameters:
        SPLITS: 분할된 텍스트 데이터 : Document

    Returns:
        텍스트 데이터
    """
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        api_key=openai.api_key,
        max_tokens=1000,
        temperature=0.0,
    )
    summaries = []
    memory = ConversationSummaryMemory(llm=llm, return_messages=True)

    count = 0
    for SPLIT in SPLITS:
        SPLIT = SPLIT.page_content

        try:
            context = memory.load_memory_variables({})["history"]
            prompt = ChatPromptTemplate.from_template(
                """
                persona : documents filter
                language : only in korean
                extract the parts related to the context and ignore the rest,
                write blanck if it's not relevant,
                
                <context>
                {context}
                </context>
                
                <docs>
                {SPLIT}
                </docs>
                """
            )
            chain = prompt | llm | StrOutputParser()
            summary = chain.invoke({"SPLIT": SPLIT, "context": context})
            memory.save_context({"input": f"summary # {count}"}, {"output": summary})
            summaries.append(summary)
            count += 1

        except Exception as e:
            # 오류 처리: 만약 API 호출 중에 문제가 발생하면 오류 메시지 추가
            print(f"Error summarizing document: {e}")
            summaries.append(f"Error summarizing document: {e}")

    return "".join(summaries)
