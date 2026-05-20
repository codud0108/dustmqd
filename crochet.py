import streamlit as st
import pandas as pd

# 1. 페이지 설정 및 디자인
st.set_page_config(
    page_title="코바늘 도안 빌더 & 영상 사전", 
    page_icon="🧶", 
    layout="wide"
)

# 디자인 커스텀 CSS
st.markdown("""
    <style>
    .main .block-container {padding-top: 2rem;}
    h1 {color: #2E5A88;}
    h2 {color: #4A7BB0;}
    .video-link { font-size: 1.1rem; font-weight: bold; color: #FF4B4B; }
    </style>
    """, unsafe_allow_value=True)

st.title("🧶 코바늘 영문 도안 번역 & 영상 연동 빌더")
st.write("영어 코바늘 용어를 배우고 영상을 보며 학습하세요! 나만의 도안을 조합하고 관리할 수 있습니다.")

# --- 데이터 정의 (코바늘 전용 데이터셋 + 유튜브 영상 링크 추가) ---
# *주의*: 실제 특정 영상 링크나 검색 결과 링크로 연결해 두었습니다. 원하시는 영상의 URL로 교체 가능합니다.
crochet_data = {
    "약어 (US)": ["ch", "sc", "hdc", "dc", "tr", "sl st", "inc", "dec/tog", "st(s)", "sp"],
    "원어 (Full Term)": ["Chain", "Single Crochet", "Half Double Crochet", "Double Crochet", "Treble Crochet", "Slip Stitch", "Increase", "Decrease / Together", "Stitch(es)", "Space"],
    "영국식 (UK)": ["ch", "dc (Double)", "htr (Half Treble)", "tr (Treble)", "dtr (Double Treble)", "ss", "inc", "dec", "st(s)", "sp"],
    "한국어 뜻": ["사슬뜨기", "짧은뜨기", "긴뜨기", "한길 긴뜨기", "두길 긴뜨기", "빼뜨기", "코늘리기 (한 코에 두 코)", "코줄이기 (모아뜨기)", "코 (Stitch)", "사슬로 생긴 공간"],
    "일본식 기호": ["◯ / ㆍ", "X / +", "T", "mp[F]", "mp[E]", "●", "V", "A", "-", "-"],
    "영상 튜토리얼 (YouTube)": [
        "https://www.youtube.com/results?search_query=crochet+chain+stitch",
        "https://www.youtube.com/results?search_query=crochet+single+crochet",
        "https://www.youtube.com/results?search_query=crochet+half+double+crochet",
        "https://www.youtube.com/results?search_query=crochet+double+crochet",
        "https://www.youtube.com/results?search_query=crochet+treble+crochet",
        "https://www.youtube.com/results?search_query=crochet+slip+stitch",
        "https://www.youtube.com/results?search_query=crochet+increase",
        "https://www.youtube.com/results?search_query=crochet+decrease",
        "https://www.youtube.com/results?search_query=crochet+stitch+count",
        "https://www.youtube.com/results?search_query=crochet+chain+space"
    ]
}
df_crochet = pd.DataFrame(crochet_data)

# 미국식 ↔ 영국식 변환용 딕셔너리 사전 매핑
us_to_uk_dict = {
    "sc": "dc", "hdc": "htr", "dc": "tr", "tr": "dtr", "sl st": "ss",
    "Single Crochet": "Double Crochet", "Half Double Crochet": "Half Treble Crochet",
    "Double Crochet": "Treble Crochet", "Treble Crochet": "Double Treble Crochet"
}
uk_to_us_dict = {v: k for k, v in us_to_uk_dict.items()}


# --- 탭 구성 ---
tab1, tab2, tab3 = st.tabs(["📚 코바늘 용어 & 영상 사전", "🔄 US ↔ UK 도안 변환기", "🛠️ 코바늘 도안 빌더"])


# --- 탭 1: 용어 사전 ---
with tab1:
    st.header("🔍 코바늘 영문 기호 & 영상 검색")
    st.write("약어를 검색하고 오른쪽 끝의 **유튜브 링크**를 클릭해 뜨는 방법을 영상으로 직접 확인해 보세요!")
    
    search_query = st.text_input("찾고 싶은 약어나 단어를 입력하세요 (예: sc, 한길 긴뜨기):", key="search")
    
    if search_query:
        filtered_df = df_crochet[
            df_crochet['약어 (US)'].str.contains(search_query, case=False) |
            df_crochet['영국식 (UK)'].str.contains(search_query, case=False) |
            df_crochet['한국어 뜻'].str.contains(search_query, case=False)
        ]
        # Link 컬럼 활성화를 위해 column_config 사용
        st.data_editor(
            filtered_df, 
            use_container_width=True, 
            hide_index=True,
            column_config={"영상 튜토리얼 (YouTube)": st.column_config.LinkColumn("📺 영상 보기", display_text="유튜브 영상 보기")}
        )
    else:
        st.data_editor(
            df_crochet, 
            use_container_width=True, 
            hide_index=True,
            column_config={"영상 튜토리얼 (YouTube)": st.column_config.LinkColumn("📺 영상 보기", display_text="유튜브 영상 보기")}
        )


# --- 탭 2: US ↔ UK 변환기 ---
with tab2:
    st.header("🔄 미국식 ↔ 영국식 도안 자동 번역기")
    st.info("💡 코바늘은 미국식과 영국식 약어가 달라 헷갈리기 쉽습니다! 전체 서술형 도안 텍스트를 통째로 바꾸어 줍니다.")
    
    direction = st.radio("변환 방향 선택", ["미국식(US) ➡️ 영국식(UK)", "영국식(UK) ➡️ 미국식(US)"])
    
    input_text = st.text_area("영어 도안 텍스트를 여기에 붙여넣으세요:", height=200, 
                              placeholder="예시: Rnd 1: 6 sc in magic ring\nRnd 2: inc in every st (12 sts)")
    
    if st.button("🪄 변환하기"):
        if input_text:
            converted_text = input_text
            mapping = us_to_uk_dict if "미국식(US) ➡️ 영국식(UK)" in direction else uk_to_us_dict
            
            for key, value in mapping.items():
                converted_text = converted_text.replace(f" {key} ", f" **{value}** ")
                converted_text = converted_text.replace(f" {key}\n", f" **{value}**\n")
                converted_text = converted_text.replace(f": {key} ", f": **{value}** ")
                converted_text = converted_text.replace(f" {key.capitalize()} ", f" **{value.capitalize()}** ")
            
            st.markdown("### 📋 변환된 도안 (변경된 부분은 두껍게 표시됩니다)")
            st.markdown(converted_text)
        else:
            st.warning("텍스트를 먼저 입력해주세요.")


# --- 탭 3: 코바늘 도안 빌더 ---
with tab3:
    st.header("📝 단별/라운드별 도안 제작기")
    st.write("선택 상자를 이용해 매 단(Row) 또는 라운드(Rnd)의 규칙을 조합해 보세요.")
    
    if "crochet_steps" not in st.session_state:
        st.session_state.crochet_steps = []

    # 입력 레이아웃 구획 나누기
    col1, col2, col3, col4 = st.columns([1, 1.5, 1, 1.5])
    
    with col1:
        type_select = st.selectbox("구분", ["Rnd (라운드)", "Row (단)"])
        num_select = st.number_input("번호", min_value=1, value=1, step=1)
        
    with col2:
        stitch_options = df_crochet["약어 (US)"].tolist() + ["직접 입력"]
        stitch_select = st.selectbox("스티치 기호", stitch_options)
        if stitch_select == "직접 입력":
            stitch_select = st.text_input("스티치 직접 입력:")
            
    with col3:
        times_select = st.number_input("반복/코 수", min_value=1, value=1, step=1)
        
    with col4:
        total_sts = st.text_input("해당 단 완성 후 총 코 수 (선택사항)", placeholder="예: 12 sts")

    # [핵심 추가] 스티치 기호를 고르면 화면에 해당 기호의 한국어 뜻과 영상 링크를 힌트로 실시간 제공!
    if stitch_select != "직접 입력":
        row_info = df_crochet[df_crochet["약어 (US)"] == stitch_select].iloc[0]
        st.markdown(f"💡 **선택한 기호 정보:** {row_info['한국어 뜻']} ({row_info['원어 (Full Term)']}) | [🎥 뜨개 방법 유튜브 영상 열기]({row_info['영상 튜토리얼 (YouTube)']})")

    # 버튼을 눌러 리스트에 기록 추가
    if st.button("➕ 도안에 이 단계 추가하기"):
        prefix = "Rnd" if "Rnd" in type_select else "Row"
        step_str = f"{prefix} {num_select}: {stitch_select} {times_select}번 반복"
        if total_sts:
            step_str += f" ({total_sts})"
            
        st.session_state.crochet_steps.append(step_str)
        st.success(f"추가됨 ➡️ {step_str}")

    # 현재 조립된 도안 출력 섹션
    st.markdown("---")
    st.markdown("### 📜 내가 만든 코바늘 도안 출력")
    
    if st.session_state.crochet_steps:
        final_pattern_text = "\n".join(st.session_state.crochet_steps)
        st.code(final_pattern_text, language="text")
        
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            st.download_button(
                label="💾 파일로 내보내기 (.txt)",
                data=final_pattern_text,
                file_name="my_crochet_pattern.txt",
                mime="text/plain"
            )
        with btn_col2:
            if st.button("🗑️ 전체 도안 삭제 (초기화)"):
                st.session_state.crochet_steps = []
                st.rerun()
    else:
        st.info("오른쪽 위의 입력창에서 단계를 조합한 후 '추가하기' 버튼을 누르면 여기에 도안이 쌓입니다.")
