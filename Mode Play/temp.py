import os
os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'

import streamlit as st
import base64
import random
import numpy as np
import io
import wave

# 이미지를 base64로 인코딩하는 함수
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

keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
mode_types = ['Ionian', 'Dorian', 'Phrygian', 'Lydian', 'Mixolydian', 'Aeolian', 'Locrian']  # mode_types 정의 추가

# 랜덤으로 키와 모드의 종류 선택
random_key = random.choice(keys)
random_mode = random.choice(mode_types)  # mode_types 사용

# 선택된 키와 모드 출력
print(f"랜덤으로 선택된 키: {random_key}, 모드: {random_mode}")

# 모드와 그에 따른 구성음 정의
modes = {
    'Ionian': [0, 2, 4, 5, 7, 9, 11],
        'Dorian': [0, 2, 3, 5, 7, 9, 10],
        'Phrygian': [0, 1, 3, 5, 7, 8, 10],
        'Lydian': [0, 2, 4, 6, 7, 9, 11],
        'Mixolydian': [0, 2, 4, 5, 7, 9, 10],
        'Aeolian': [0, 2, 3, 5, 7, 8, 10],
        'Locrian': [0, 1, 3, 5, 6, 8, 10]

}

# 모드에 따른 구성음 생성 함수
def generate_mode_notes(base_note, mode):
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    # 옥타브를 포함한 음계 리스트 생성
    full_notes = [note + str(octave) for octave in range(0, 8) for note in notes]
    
    # base_note에서 옥타브 정보를 제거
    base_note_without_octave = base_note[:-1] if base_note[-1].isdigit() else base_note

    if base_note_without_octave not in notes:
        raise ValueError(f"'{base_note}' is not in the list of valid notes.")
    
    base_index = notes.index(base_note_without_octave)
    base_index = notes.index(base_note)
    intervals = {
        'Ionian': [2, 2, 1, 2, 2, 2, 1],
        'Dorian': [2, 1, 2, 2, 2, 1, 2],
        'Phrygian': [1, 2, 2, 2, 1, 2, 2],  # Phrygian 모드 추가
        'Lydian': [2, 2, 2, 1, 2, 2, 1],
        'Mixolydian': [2, 2, 1, 2, 2, 1, 2],
        'Aeolian': [2, 1, 2, 2, 1, 2, 2],  # Aeolian 모드 추가
        'Locrian': [1, 2, 2, 1, 2, 2, 2]
    }
    mode_intervals = intervals[mode]  # 수정된 코드
    mode_notes = []
    for interval in mode_intervals:
        note_index = (base_index + interval) % 12
        octave = 4  # 기 옥타브를 4로 설정
        if (base_index + interval) // 12 > 0:
            octave += 1
        note = f"{notes[note_index]}{octave}"
        mode_notes.append(note)
    return mode_notes

def generate_correct_answer(key, mode_type):
    # 필요한 모드의 음정 패턴만 남김
    intervals = {
        'Ionian': [2, 2, 1, 2, 2, 2, 1],
        'Dorian': [2, 1, 2, 2, 2, 1, 2],
        'Phrygian': [1, 2, 2, 2, 1, 2, 2],
        'Lydian': [2, 2, 2, 1, 2, 2, 1],
        'Mixolydian': [2, 2, 1, 2, 2, 1, 2],
        'Aeolian': [2, 1, 2, 2, 1, 2, 2],  # Aeolian 모드 추가
        'Locrian': [1, 2, 2, 1, 2, 2, 2]
    }

    # 모드 타입이 intervals에 있는지 확인
    if mode_type not in intervals:
        raise ValueError(f"Invalid mode type: {mode_type}")

    # 음정 계산
    chord_notes = []
    current_note = key
    for interval in intervals[mode_type]:
        chord_notes.append(current_note)
        current_note = str(current_note)  # current_note를 정수로 변환
        current_note += str(interval)
        current_note = str(current_note)  # 다시 문자열로 변환

    return chord_notes

def generate_inversions(chord_notes):
    inversions = []
    for i in range(len(chord_notes)):
        inversion = chord_notes[i:] + [raise_octave(note) for note in chord_notes[:i]]
        inversions.append(inversion)
    
    ascending = sum(inversions, [])
    descending = ascending[::-1]
    
    return ascending + descending

def raise_octave(note):
    note_name, octave = note[:-1], int(note[-1])
    return f"{note_name}{octave + 1}"

def note_to_freq(note):
    # 음계 리스트 정의
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    
    # note에서 옥타브 정보를 분리
    if note[-1].isdigit():
        note_name = note[:-2] if note[-2].isdigit() else note[:-1]
        octave = int(note[-2:]) if note[-2].isdigit() else int(note[-1])
    else:
        note_name = note
        octave = 4  # 기본 옥타브를 4로 설정

    # 입력 검증
    if note_name not in notes:
        raise ValueError(f"'{note}' is not in the list of valid notes.")
    
    # 옥타브 범위 검증
    if not (0 <= octave <= 8):
        raise ValueError(f"'{note}' has an invalid octave: {octave}. Valid range is 0-8.")
    
    # 음계 인덱스 찾기
    semitones = notes.index(note_name)
    
    # 주파수 계산 (예시)
    base_freq = 440.0  # A4의 주파수
    note_freq = base_freq * (2 ** ((semitones + (octave - 4) * 12) / 12.0))
    
    return note_freq

def create_sine_wave(freq, duration, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    return np.sin(2 * np.pi * freq * t)

def create_chord_audio(frequencies, duration=1, sample_rate=44100):
    chord = np.zeros(int(sample_rate * duration))
    for freq in frequencies:
        chord += create_sine_wave(freq, duration, sample_rate)
    chord = chord / np.max(np.abs(chord))  # Normalize
    return (chord * 32767).astype(np.int16)

def create_arpeggio_audio(frequencies, bpm):
    # 예시: 오디오 데이터를 numpy 배열로 변환
    audio_data = np.array([generate_wave(frequency, bpm) for frequency in frequencies])
    return audio_data

def get_audio_base64(audio_data, sample_rate=44100):
    buffer = io.BytesIO()
    with wave.open(buffer, 'wb') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 2 bytes per sample
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_data.tobytes())
    
    return base64.b64encode(buffer.getvalue()).decode()

# 세션 상태 초기화
if 'key' not in st.session_state:
    st.session_state.key = random.choice(keys)

if 'mode_type' not in st.session_state:
    st.session_state.mode_type = random.choice(mode_types)

if 'chord_notes' not in st.session_state:
    st.session_state.chord_notes = generate_correct_answer(st.session_state.key, st.session_state.mode_type)

if 'bpm' not in st.session_state:
    st.session_state.bpm = 120

if 'mode_notes' not in st.session_state:
    st.session_state.mode_notes = generate_mode_notes(st.session_state.key, st.session_state.mode_type)  # 기본 키는 C로 설정

def get_mode_notes(mode, key):
    # 특정 키에 따른 모드의 구성음 반환하는 로직 추가
    mode_scales = {
        
    }
    
    # 키에 따른 음계의 기본 음을 설정
    note_mapping = {
        'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5, 'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'B': 11
    }
    
    scale = mode_scales.get(mode, [])
    root_note = note_mapping.get(key, 0)  # 기본 키는 C로 설정

    return [(root_note + step) % 12 for step in scale]  # 특정 키에 맞춰 조정된 구성음 반환

# Streamlit 앱 UI (헤더 텍스트 변경 및 크기 축소)
st.markdown("<h3 style='text-align: center; font-family: \"Times Newer Roman\", Times, serif;'>ChordPlay</h3>", unsafe_allow_html=True)

# 전체 레이아웃을 3개의 열로 나누 중앙 정렬
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # 새로고침 버튼
    st.markdown('<div class="refresh-button-container">', unsafe_allow_html=True)
    if st.button('🔄', key='refresh'):
        st.session_state.key = random.choice(keys)
        st.session_state.mode_type = random.choice(mode_types)
        st.session_state.chord_notes = generate_correct_answer(st.session_state.key, st.session_state.mode_type)
        st.session_state.mode_notes = generate_mode_notes(st.session_state.key, st.session_state.mode_type)  # 기본 키는 C로 설정
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Key와 코드 유형 표시 부분
    st.markdown(f"""
    <div class="center-container">
        <div class="key-style">{st.session_state.key}</div>
        <div class="chord-type-style">{st.session_state.mode_type}</div>
    </div>
    """, unsafe_allow_html=True)

    # Inversion Arpeggio 체크박스
    include_inversions = st.checkbox('Inversion Arpeggio', key='include_inversions')

    # BPM 슬라이더 (더 작게 구현, 라벨 제거)
    bpm = st.slider('BPM', 60, 240, st.session_state.bpm, format="%d", step=1, label_visibility='collapsed')
    st.session_state.bpm = bpm

    # 코드 재생 버튼
    if st.button('Answer Generation', key='play_chord'):
        frequencies = [note_to_freq(note) for note in st.session_state.chord_notes]
        if include_inversions:
            chord_notes = generate_inversions(st.session_state.chord_notes)
            frequencies = [note_to_freq(note) for note in chord_notes]
            audio_data = create_arpeggio_audio(frequencies, bpm)
        else:
            audio_data = create_chord_audio(frequencies, duration=2)  # 코드 지속 시간을 2초로 변경
        
        st.audio(audio_data, sample_rate=44100)

    # 구성음 확인 토글
    show_notes = st.toggle('Show Notes', key='toggle_show_notes')

    # 구성음 표시
    if show_notes:
        notes_text = ' '.join([note[:-1] for note in st.session_state.chord_notes])
        st.write(f"Notes: {notes_text}")

# 모드 선택  구성음 재생 버 추가
# mode_type = st.selectbox('Select Mode', ['Ionian', 'Dorian', 'Phrygian', ...])

# selected_mode 변수를 사용하지 않고 기본 모드를 정
default_mode = 'Ionian'  # 기본 모드를 Ionian으로 설정

# st.session_state.key가 올바른 음인지 확인
base_note = st.session_state.key if 'key' in st.session_state else 'C'  # 기본 음을 C로 설정

mode_notes = generate_mode_notes(base_note, default_mode)

# frequencies 변수를 초기화
frequencies = []

# st.session_state.chord_notes가 비어 있지 않은지 확인
if 'chord_notes' in st.session_state and st.session_state.chord_notes:
    try:
        # 주파수 리스트 생성
        frequencies = [note_to_freq(note) for note in st.session_state.chord_notes]
    except ValueError as e:
        st.error(str(e))
        frequencies = []
else:
    st.error("No chord notes available.")

# frequencies 변수가 비어있지 않은지 확인
if frequencies:
    ascending_audio = create_arpeggio_audio(frequencies, st.session_state.bpm)
    st.audio(ascending_audio, sample_rate=44100)
else:
    st.error("No valid frequencies to create audio.")
    ascending_audio = None  # ascending_audio 변수를 초기화

# 상승 및 하강 음 재생
descending_audio = create_arpeggio_audio(frequencies[::-1], st.session_state.bpm)

# 오디오 재생
st.audio(ascending_audio, sample_rate=44100)
st.audio(descending_audio, sample_rate=44100)

# 저작권 정보 추가
st.markdown('<div class="copyright">ⓒ 2024 Youjung Huh All Rights Reserved.</div>', unsafe_allow_html=True)




































