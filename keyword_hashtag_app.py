
import streamlit as st
import pandas as pd
import itertools
from collections import Counter

st.title("🧼 키워드/해시태그 자동 정리기")

st.markdown("""
안녕하세요! 👋  
엑셀 파일을 업로드하면 키워드를 자동으로 정리해주는 툴이에요.

### ✅ 사용 방법
1. 엑셀 파일을 업로드하세요  
   - A열 A2부터 키워드가 한 셀씩 들어 있어야 해요
2. 원하는 행 수를 입력하세요 (예: 100)
3. 변환된 결과를 엑셀 파일로 다운로드하세요 ✅

### 📋 출력 결과
- **키워드**: 3개씩 묶어서 콤마(,)로 구분 → 한 행에 하나씩
- **해시태그**: 상위 10개 키워드를 쉼표로 이어붙여 B열 첫 행에 표시

### 📌 참고
- 키워드가 부족하면 자동으로 반복해서 채워져요
- 해시태그는 '#' 없이 단어만 쉼표로 연결돼요

문의사항은 언제든지 연락 주세요 💌  
""")

uploaded_file = st.file_uploader("엑셀 파일을 업로드하세요", type=["xlsx"])
row_limit = st.number_input("몇 행까지 키워드 데이터를 만들까요?", min_value=1, max_value=1000, value=100, step=10)

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file, usecols=[0], skiprows=1, header=None)
        keyword_list = df[0].dropna().astype(str).tolist()

        while len(keyword_list) < row_limit * 3:
            keyword_list.extend(keyword_list)

        keyword_groups = list(itertools.islice(itertools.zip_longest(*[iter(keyword_list)]*3), row_limit))
        keyword_column = [','.join(filter(None, group)) for group in keyword_groups]

        keyword_freq = Counter(keyword_list)
        top_30_keywords = [kw for kw, _ in keyword_freq.most_common(30)]
        top_10 = top_30_keywords[:10]
        hashtag_string = ','.join(top_10)

        hashtag_column = [''] * row_limit
        hashtag_column[0] = hashtag_string

        result_df = pd.DataFrame({
            '키워드': keyword_column,
            '해시태그': hashtag_column
        })

        st.subheader("📋 처리 결과 미리보기")
        st.dataframe(result_df)

        from io import BytesIO
        output = BytesIO()
        result_df.to_excel(output, index=False)
        st.download_button(
            label="📥 엑셀 다운로드",
            data=output.getvalue(),
            file_name="정리된_키워드_해시태그.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        st.error(f"❌ 파일을 처리하는 중 오류가 발생했어요: {e}")
