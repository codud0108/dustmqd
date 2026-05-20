import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="코바늘/대바늘 도안 빌더", page_icon="🧶", layout="wide")

st.title("🧶 영문 뜨개 도안 번역 & 제작 빌더")
st.write("영어 뜨개 용어를 배우고, 나만의 도안을 조합해 보세요!")

# 2. 데이터 정의 (자주 쓰이는 영문 약어 및 기호)
knitting_dict = {
    "Abbreviation (약어)": ["K", "P", "YO", "K2tog", "SSK", "St(s)", "Rep", "Sl 1"],
    "Full Term (원어)": ["Knit", "Purl", "Yarn Over", "Knit 2 together", "Slip Slip Knit", "Stitch(es)", "Repeat", "Slip 1 stitch"],
    "Korean (한국어)": ["겉뜨기", "안뜨기", "바늘비우기", "왼코 모아뜨기 (2코를 같이)", "오른코 모아뜨기", "코", "반복", "한 코 걸러뜨기"],
    "Symbol (기호)": ["|", "—", "◯", "人", "入", "st", "*", "V"]
}
df_dict = pd.DataFrame(knitting_dict)

# 3. 탭 구성
tab1, tab2 = st.tabs(["📚 영문 용어 사전", "🛠️ 도안 제작기 (Builder)"])

# --- 탭 1: 용어 사전 ---
with tab1:
    st.header("🔍 영문 뜨개 기호 & 용어 검색")
    
    # 검색 기능
    search_query = st.text_input("찾고 싶은 영문 약어나 뜻을 입력하세요 (예: K, 안뜨기):")
    
    if search_query:
        filtered_df = df_dict[
            df_dict['Abbreviation (약어)'].str.contains(search_query, case=False) |
            df_dict['Korean (한국어)'].str.contains(search_query, case=False)
        ]
        st.dataframe(filtered_df, use_container_width=True)
    else:
        st.dataframe(df_dict, use_container_width=True)

# --- 탭 2: 도안 제작기 ---
with tab2:
    st.header("📝 나만의 도안 조합하기")
    st.write("원하는 스티치와 반복 횟수를 선택해 단(Row)별 도안을 완성해 보세요.")

    # 세션 상태를 이용해 도안 단계 저장
    if "pattern_steps" not in st.session_state:
        st.session_state.pattern_steps = []

    # 입력 폼
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        stitch = st.selectbox("스티치 선택", df_dict["Abbreviation (약어)"].tolist() + ["직접 입력"])
        if stitch == "직접 입력":
            stitch = st.text_input("커스텀 스티치 입력:")
            
    with col2:
        count = st.number_input("횟수/코 수", min_value=1, value=1, step=1)
        
    with col3:
        row_num = st.number_input("단 (Row) 번호", min_value=1, value=1, step=1)

    # 도안 추가 버튼
    if st.button("➕ 도안에 단계 추가"):
        step_text = f"Row {row_num}: {stitch} {count} times" if count > 1 else f"Row {row_num}: {stitch}"
        st.session_state.pattern_steps.append(step_text)
        st.success(f"'{step_text}' 가 추가되었습니다!")

    # 현재 제작된 도안 표시
    st.markdown("### 📋 현재 작성된 도안")
    if st.session_state.pattern_steps:
        # 단별로 예쁘게 출력
        full_pattern = "\n".join(st.session_state.pattern_steps)
        st.code(full_pattern, language="text")
        
        # 초기화 버튼
        if st.button("🗑️ 전체 초기화"):
            st.session_state.pattern_steps = []
            st.rerun()
            
        # 텍스트 파일로 다운로드 기능
        st.download_button(
            label="💾 도안 다운로드 (.txt)",
            data=full_pattern,
            file_name="my_knitting_pattern.txt",
            mime="text/plain"
        )
    else:
        st.info("아직 추가된 도안 단계가 없습니다. 위에서 스티치를 선택해 보세요!")
