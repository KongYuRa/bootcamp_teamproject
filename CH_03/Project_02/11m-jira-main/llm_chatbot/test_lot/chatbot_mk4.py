from llm_module.docs_utils import *
from llm_module.db_utils import *
from llm_module.script_utils import *
from llm_module.llm_utils import *
from llm_module.translator_module import translator
import random


json_files = [
    "./llm_chatbot/documents/filtered_unsolved_cases.json",
    "./llm_chatbot/documents/korea_crime.json",
]
titles = title_json_data(json_files)
sample_titles = titles[0:11]

store = {}
ID = "test31"
# LANG_CODE = "jpn_Jpan"
LANG_CODE = False
LANG = "korean"


while True:
    print("================================")
    path = "./llm_chatbot/db/script_db"
    db_name = "script_db"
    script_db = load_vstore(db_name, path)
    query = input("어떤 이야기가 듣고 싶으신가요?")
    print(query)

    if query.lower() == "exit":
        print("대화를 종료합니다.")
        query = False
        break
    elif query is None or "아무거나" in query.strip():
        print("재미난 이야기를 가져오는 중...")
        choice = random.choice(sample_titles)
        query = choice
        print(choice)

    relavence = evaluator(query, script_db)
    print(relavence[0])
    if relavence[0] < 80:
        print(
            "모르는 이야기 입니다.",
            "종료 : exit",
            "다시 물어보기 : return",
            "생성하기 : create",
        )
        user_input = input("입력하세요.")
        if user_input.lower() == "exit":
            print("대화를 종료합니다.")
            query = False
            break
        elif user_input.lower() == "return":
            continue

        elif user_input.lower() == "create":
            text_input = input("URL 또는 텍스트를 입력해주세요.")
            new_script = script_maker(text_input)
            add_to_vstore(new_script, script_db)
            print("생성이 완료되었습니다.", "다시 답변해주세요.")
            continue

    elif relavence[0] < 95 and relavence[0] >= 80:
        print("더 자세히 이야기 해주세요")
        continue
    elif relavence[0] >= 95:
        script = relavence[1]
        break

if query:
    chain = chain_maker(script, LANG)
    h_chain = history_chain(chain, store)
    response = h_chain.stream(
        # 질문 입력
        {"question": query},
        # 세션 ID 기준으로 대화를 기록합니다.
        config={"configurable": {"session_id": ID}},
    )
    print("\n답변:")
    for chunk in response:
        print(chunk, end="", flush=True)

    while True:
        print("\n========================\n")
        query = input("반응을 입력하세요.")
        if query.lower() == "exit":
            print("대화를 종료합니다.")
            break
        response = h_chain.stream(
            # 질문 입력
            {"question": query},
            # 세션 ID 기준으로 대화를 기록합니다.
            config={"configurable": {"session_id": ID}},
        )
        if LANG_CODE:
            print(translator(query, LANG_CODE))
        else:
            print(query)
        print("\n답변:")
        for chunk in response:
            print(chunk, end="", flush=True)
