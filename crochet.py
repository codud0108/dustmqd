import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(
    page_title="코바늘 블록 도안 빌더", 
    page_icon="🧶", 
    layout="wide"
)

st.title("🧶 코바늘 영문 도안 번역 & 블록형 빌더")
st.write("도안을 블록 형태로 쌓고, 추가된 단계를 언제든 자유롭게 수정하거나 삭제해 보세요!")

# --- 데이터 정의 (코바늘 데이터셋) ---
crochet_data = {
    "약어 (US)": ["ch", "sc", "hdc", "dc", "tr", "sl st", "inc", "dec/tog", "st(s)", "sp"],
    "원어 (Full Term)": ["Chain", "Single Crochet", "Half Double Crochet", "Double Crochet", "Treble Crochet", "Slip Stitch", "Increase", "Decrease / Together", "Stitch(es)", "Space"],
    "영국식 (UK)": ["ch", "dc (Double)", "htr (Half Treble)", "tr (Treble)", "dtr (Double Treble)", "ss", "inc", "dec", "st(s)", "sp"],
    "한국어 뜻": ["사슬뜨기", "짧은뜨기", "긴뜨기", "한길 긴뜨기", "두길 긴뜨기", "빼뜨기", "코늘리기 (한 코에 두 코)", "코줄이기 (모아뜨기)", "코 (Stitch)", "사슬로 생긴 공간"],
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

us_to_uk_dict = {
    "sc": "dc", "hdc": "htr", "dc": "tr", "tr": "dtr", "sl st": "ss",
    "Single Crochet": "Double Crochet", "Half Double Crochet": "Half Treble Crochet",
    "Double Crochet": "Treble Crochet", "Treble Crochet": "Double Treble Crochet"
}
uk_to_us_dict = {v: k for k, v in us_to_uk_dict.items()}


# --- 탭 구성 ---
tab1, tab2, tab3 = st.tabs(["📚 코바늘 용어 & 영상 사전", "🔄 US ↔ UK 도안 변환기", "🛠️ 블록형 도안 빌더"])


# --- 탭 1: 용어 사전 ---
with tab1:
    st.subheader("🔍 코바늘 영문 기호 & 영상 검색")
    search_query = st.text_input("찾고 싶은 약어나 단어를 입력하세요:", key="search")
    
    if search_query:
        filtered_df = df_crochet[
            df_crochet['약어 (US)'].str.contains(search_query, case=False) |
            df_crochet['영국식 (UK)'].str.contains(search_query, case=False) |
            df_crochet['한국어 뜻'].str.contains(search_query, case=False)
        ]
        st.data_editor(filtered_df, use_container_width=True, hide_index=True,
                       column_config={"영상 튜토리얼 (YouTube)": st.column_config.LinkColumn("📺 영상 보기", display_text="유튜브 영상 보기")})
    else:
        st.data_editor(df_crochet, use_container_width=True, hide_index=True,
                       column_config={"영상 튜토리얼 (YouTube)": st.column_config.LinkColumn("📺 영상 보기", display_text="유튜브 영상 보기")})


# --- 탭 2: US ↔ UK 변환기 ---
with tab2:
    st.subheader("🔄 미국식 ↔ 영국식 도안 자동 번역기")
    direction = st.radio("변환 방향 선택", ["미국식(US) ➡️ 영국식(UK)", "영국식(UK) ➡️ 미국식(US)"])
    input_text = st.text_area("영어 도안 텍스트를 여기에 붙여넣으세요:", height=150)
    
    if st.button("🪄 변환하기"):
        if input_text:
            converted_text = input_text
            mapping = us_to_uk_dict if "미국식(US) ➡️ 영국식(UK)" in direction else uk_to_us_dict
            for key, value in mapping.items():
                converted_text = converted_text.replace(f" {key} ", f" **{value}** ")
                converted_text = converted_text.replace(f" {key}\n", f" **{value}**\n")
                converted_text = converted_text.replace(f": {key} ", f": **{value}** ")
                converted_text = converted_text.replace(f" {key.capitalize()} ", f" **{value.capitalize()}** ")
            st.markdown("### 📋 변환된 도안")
            st.markdown(converted_text)


# --- 탭 3: 블록형 도안 빌더 (핵심 업데이트) ---
with tab3:
    st.subheader("📝 블록형 도안 제작 및 실시간 수정")
    st.write("💡 아래에서 단계를 추가한 후, **생성된 테이블 블록의 칸을 더블클릭**하면 도안을 바로 수정할 수 있습니다!")

    # 세션 상태에 딕셔너리 리스트 구조로 도안 저장 (표 형태로 변환하기 위함)
    if "pattern_blocks" not in st.session_state:
        st.session_state.pattern_blocks = []

    # 1. 도안 단계 입력창
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1.5, 1, 1.5])
    
    with col1:
        type_select = st.selectbox("구분", ["Rnd", "Row"])
    with col2:
        num_select = st.number_input("번호", min_value=1, value=1, step=1)
    with col3:
        stitch_options = df_crochet["약어 (US)"].tolist() + ["직접 입력"]
        stitch_select = st.selectbox("스티치 기호", stitch_options)
        if stitch_select == "직접 입력":
            stitch_select = st.text_input("스티치 직접 입력:")
    with col4:
        times_select = st.number_input("반복 횟수", min_value=1, value=1, step=1)
    with col5:
        total_sts = st.text_input("총 코 수 (선택)", placeholder="예: 12 sts")

    # 영상 힌트 링크
    if stitch_select in df_crochet["약어 (US)"].tolist():
        row_info = df_crochet[df_crochet["약어 (US)"] == stitch_select].iloc[0]
        st.markdown(f"💡 **기호 힌트:** {row_info['한국어 뜻']} | [🎥 영상 학습 하기]({row_info['영상 튜토리얼 (YouTube)']})")

    # 단계 추가 버튼
    if st.button("➕ 도안에 블록 추가"):
        new_block = {
            "구분": type_select,
            "번호": num_select,
            "스티치": stitch_select,
            "반복 횟수": times_select,
            "총 코 수": total_sts if total_sts else ""
        }
        st.session_state.pattern_blocks.append(new_block)
        st.success("블록이 추가되었습니다!")

    # 2. 블록 출력 및 실시간 수정 영역
    st.markdown("---")
    st.markdown("### 📊 작성된 도안 블록 리스트")

    if st.session_state.pattern_blocks:
        # 리스트 데이터를 데이터프레임으로 변환
        df_pattern = pd.DataFrame(st.session_state.pattern_blocks)
        
        # [핵심] st.data_editor를 사용하여 사용자가 표 안에서 직접 텍스트 수정 가능하게 만듦
        edited_df = st.data_editor(
            df_pattern,
            use_container_width=True,
            num_rows="dynamic",  # 사용자가 맨 밑 빈칸을 통해 행을 추가하거나 행을 선택해 Delete 키로 삭제 가능
            column_config={
                "구분": st.column_config.SelectboxColumn("구분", options=["Rnd", "Row"], required=True),
                "스티치": st.column_config.SelectboxColumn("스티치", options=df_crochet["약어 (US)"].tolist() + ["직접 입력"])
            }
        )
        
        # 사용자가 수정한 데이터를 세션 상태에 즉시 반영
        st.session_state.pattern_blocks = edited_df.to_dict(orient="records")

        # 3. 최종 텍스트 프리뷰 및 파일 다운로드
        st.markdown("### 📜 최종 텍스트 도안 미리보기")
        final_lines = []
        for b in st.session_state.pattern_blocks:
            # 딕셔너리 데이터 유효성 검사 (삭제된 행 방지)
            if pd.isna(b.get("구분")) or b.get("구분") is None:
                continue
            sts_part = f" ({b['총 코 수']})" if b.get('총 코 수') else ""
            line = f"{b['구분']} {int(b['번호'])}: {b['스티치']} {int(b['반복 횟'])}times{sts_part}"
            final_lines.append(line)
        
        final_text = "\n".join(final_lines)
        st.code(final_text, language="text")

        # 파일 다운로드 및 초기화 버튼
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            st.download_button(
                label="💾 완성된 도안 다운로드 (.txt)",
                data=final_text,
                file_name="my_block_pattern.txt",
                mime="text/plain"
            )
        with btn_col2:
            if st.button("🗑️ 전체 블록 초기화"):
                st.session_state.pattern_blocks = []
                st.rerun()
    else:
        st.info("추가된 도안 블록이 없습니다. 위에서 스티치를 조합해 블록을 추가해 보세요!")
