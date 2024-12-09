import os
import warnings
import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

os.environ["TOKENIZERS_PARALLELISM"] = "false"
warnings.filterwarnings("ignore", category=FutureWarning)


def translator(TEXT, LANG_CODE='kor_Hang'):
    """
    텍스트 다국어 번역

    Parameters :

    LANG_CODE: eng_Latn, jpn_Jpan, kor_Hang, spa_Latn

    Returns : 번역되 텍스트
    """
    model_name = "facebook/nllb-200-distilled-600M"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    inputs = tokenizer(TEXT, return_tensors="pt")
    generated_tokens = model.generate(
        inputs.input_ids, forced_bos_token_id=tokenizer.lang_code_to_id[LANG_CODE]
    )
    translated_text = tokenizer.decode(generated_tokens[0], skip_special_tokens=True)
 
    return translated_text

import io
import requests
from pydub import AudioSegment
from pydub.playback import play

def audio_generator(TEXT):
    """
    입력된 텍스트를 음성으로 변환

    Parameters : 텍스트

    Returns : mp3 음성
    """
    
    api_key = os.environ.get('ElevenLabs_API_KEY')
    url = "https://api.elevenlabs.io/v1/text-to-speech/ZJCNdZEjYwkOElxugmW2/stream"
    # url = "https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/stream"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }
    data = {
        "text": TEXT,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.3,
            "similarity_boost": 1,
            "style": 1,
            "use_speaker_boost": True
        }
    }

    response = requests.post(url, json=data, headers=headers, stream=True)

    if response.status_code == 200:
        # api 요청 성공 == 200
        audio_content = b""

        # 청크 단위로 뎅터 처리 - 대용량 데이터 처리 시
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                audio_content += chunk
        segment = AudioSegment.from_mp3(io.BytesIO(audio_content))
        return segment