
import streamlit as st
import pandas as pd
import itertools
from collections import Counter

st.title("🧼 키워드/해시태그 자동 정리기")

uploaded_file = st.file_uploader("엑셀 파일을 업로드하세요", type=["xlsx"])
row_limit = st.number_input("몇 행까지 키워드 데이터를 만들까요?", min_value=1, max_value=1000, value=100, step=10)

if uploaded_file is not None:
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
