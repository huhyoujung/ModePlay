import os
os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'

import streamlit as st
import random
import numpy as np
import wave
import base64

def img_to_base64(img_path):
    with open(img_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

# 로고 이미지를 base64로 인코딩
logo_base64 = img_to_base64("logo.png")

# 파비콘 설정
favicon_base64 = img_to_base64("logo.png")
st.set_page_config(page_title="ChordPlay", page_icon=f"data:image/png;base64,{favicon_base64}", layout="wide")

# CSS를 사용하여 폰트와 배경색 설정
st.markdown(f"""
    <style>
    @import url('https://timesnewerroman.com/TNR.css');

    /* 전체 앱에 라이트 모드 스타일 적용 */
    .stApp {{
        background-color: white;
        color: black;
    }}

    /* 기본 폰트 설정 */
    body, .stButton>button, .stTextInput>div>div>input, .stSelectbox, p, h1, h2, h3, h4, h5, h6 {{
        font-family: 'Times Newer Roman', Times, serif;
        color: black;
    }}

    /* 버튼 스타일 */
    .stButton>button {{
        background-color: white;
        color: black;
        border-color: black;
    }}

    .stButton>button:hover {{
        background-color: #f0f0f0;
    }}

    /* 체크박스 스타일 */
    .stCheckbox {{
        color: black;
    }}
    .stCheckbox [data-baseweb="checkbox"] {{
        background-color: white;
        border-color: black;
    }}
    .stCheckbox [data-baseweb="checkbox"] div[data-checked="true"] {{
        background-color: black;
    }}

    /* 슬라이더 스타일 */
    .stSlider [data-baseweb="slider"] div[role="slider"] {{
        background-color: black;
    }}

    /* 키 스타 */
    .key-style {{
        border: 2px solid black;
        color: black;
        background-color: white;
        padding: 10px 20px;
        border-radius: 50px;
        display: inline-block;
        font-size: 24px;
        font-weight: bold;
        margin-right: 10px;
    }}

    /* 코드 타입 스타일 */
    .chord-type-style {{
        color: white;
        background-color: black;
        padding: 10px 20px;
        border-radius: 50px;
        display: inline-block;
        font-size: 24px;
        font-weight: bold;
        margin-left: 10px;
    }}

    /* 중앙 정렬 컨테이너 */
    .center-container {{
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 20px;
    }}

    /* 저작권 정보 */
    .copyright {{
        position: fixed;
        left: 0;
        bottom: 10px;
        width: 100%;
        text-align: center;
        font-size: 12px;
        color: #888;
    }}

    /* 새로고침 버튼 컨테이너 */
    .refresh-button-container {{
        display: flex;
        justify-content: center;
        margin-bottom: 10px;
    }}

    /* 로고 이미지 */
    .logo-img {{
        display: block;
        margin: 0 auto;
        width: 100px;
        height: auto;
    }}

    /* 다크모  버튼 숨기기 */
    [data-testid="stToolbar"] {{
        display: none;
    }}
    </style>
    
    <!-- 로고 이미지 추가 -->
    <img src="data:image/png;base64,{logo_base64}" class="logo-img">
    """, unsafe_allow_html=True)

# 모드와 그에 따른 음계 (첫 음의 옥타브 추가)
modes = {
    'Ionian': [0, 2, 4, 5, 7, 9, 11, 12],  # 첫 음의 옥타브 추가
    'Dorian': [0, 2, 3, 5, 7, 9, 10, 12],
    'Phrygian': [0, 1, 3, 5, 7, 8, 10, 12],
    'Lydian': [0, 2, 4, 6, 7, 9, 11, 12],  # 4도에 샵이 붙음
    'Mixolydian': [0, 2, 4, 5, 7, 9, 10, 12],
    'Aeolian': [0, 2, 3, 5, 7, 8, 10, 12],
    'Locrian': [0, 1, 3, 5, 6, 8, 10, 12]
}

# 12키
keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
key_names = ['C', 'C♯', 'D', 'D♯', 'E', 'F', 'F♯', 'G', 'G♯', 'A', 'A♯', 'B']

# 플랫 및 샵 음계 표기
def get_note_name(note):
    if note == 0:
        return 'C'
    elif note == 1:
        return 'C♭'
    elif note == 2:
        return 'C♯'
    elif note == 3:
        return 'D♭'
    elif note == 4:
        return 'D'
    elif note == 5:
        return 'D♯'
    elif note == 6:
        return 'E♭'
    elif note == 7:
        return 'E'
    elif note == 8:
        return 'F♭'
    elif note == 9:
        return 'F'
    elif note == 10:
        return 'F♯'
    elif note == 11:
        return 'G♭'
    elif note == 12:
        return 'G'
    elif note == 13:
        return 'G♯'
    elif note == 14:
        return 'A♭'
    elif note == 15:
        return 'A'
    elif note == 16:
        return 'A♯'
    elif note == 17:
        return 'B♭'
    elif note == 18:
        return 'B'
    return key_names[note]

# 세션 상태 초기화
if 'random_key' not in st.session_state:
    st.session_state.random_key = random.choice(keys)
if 'random_mode' not in st.session_state:
    st.session_state.random_mode = random.choice(list(modes.keys()))

# 선택된 모드와 키에 따른 음계 생성
def generate_scale(key, mode):
    base_note = keys.index(key)
    scale = [(base_note + interval) % 12 for interval in modes[mode]]
    return scale

# WAV 파일로 음원 생성
def generate_wave(frequency, duration, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = 0.5 * np.sin(2 * np.pi * frequency * t)
    return wave

# 음계를 WAV 파일로 저장
def save_scale_as_wav(scale, filename='scale.wav', duration=0.5):
    sample_rate = 44100
    audio_data = []

    # 현재 음을 기준으로 한 옥타브 조정
    current_note = scale[0]  # 첫 음을 기준으로 설정
    for note in scale:
        # 현재 음보다 낮은 음이 나올 경우 한 옥타브 올리기
        if note < current_note:
            note += 12  # 한 옥타브 올리기
        audio_data.append(generate_wave(440 * 2 ** ((note - 9) / 12), duration))
        current_note = note  # 현재 음 업데이트

    audio_data = np.concatenate(audio_data)
    
    # WAV 파일로 저장
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)  # mono
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(sample_rate)
        wf.writeframes((audio_data * 32767).astype(np.int16))

# Streamlit을 사용하여 결과 출력
st.write(f"Current Key: {st.session_state.random_key}")
st.write(f"Current Mode: {st.session_state.random_mode}")

# "Key Randomize" 버튼을 눌렀을 때 키 새로 고침
if st.button("Key Randomize"):
    st.session_state.random_key = random.choice(keys)

# "Mode Randomize" 버튼을 눌렀을 때 모드 새로 고침
if st.button("Mode Randomize"):
    st.session_state.random_mode = random.choice(list(modes.keys()))

# "Answer Generation" 버튼을 눌렀을 때 음계 생성 및 재생
if st.button("Answer Generation"):
    scale = generate_scale(st.session_state.random_key, st.session_state.random_mode)

    # 음계의 구성음을 표시 (1~8로 표시)
    scale_with_names = []
    for i, note in enumerate(scale):
        note_name = key_names[note]
        if st.session_state.random_mode == 'Lydian' and i == 3:  # 4도에 샵 표시
            scale_with_names.append(f"{i + 1}♯")  # 4도에 샵
        else:
            scale_with_names.append(f"{i + 1}")  # 나머지는 숫자만 표시


    # 음계를 WAV 파일로 저장
    save_scale_as_wav(scale)
    
    # Streamlit에서 오디오 재생
    with open('scale.wav', 'rb') as audio_file:
        st.audio(audio_file.read(), format='audio/wav')

def create_audio_data(frequencies, bpm):
    audio_data = np.array([generate_wave(frequency, bpm) for frequency in frequencies])
    return audio_data
