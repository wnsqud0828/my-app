import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import rcParams

# 한글 폰트 설정
matplotlib.rcParams['font.family'] = 'NanumGothic'
matplotlib.rcParams['axes.unicode_minus'] = False

# 파일 업로드
st.title("전국 중학생 비율 분석")
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요:", type="csv")

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file, encoding='euc-kr')

    # 중학생 연령대 추출
    middle_school_ages = ['2024년06월_계_12세', '2024년06월_계_13세', '2024년06월_계_14세']

    # 모든 지역 데이터 처리
    results = []

    for _, row in data.iterrows():
        region = row['행정구역']
        # 중학생 연령대 인구수 합계
        middle_school_population = row[middle_school_ages].apply(lambda x: x.replace(',', '').astype(int)).sum()

        # 총 인구수
        total_population = int(row['2024년06월_계_총인구수'].replace(',', ''))

        # 비율 계산
        middle_school_ratio = (middle_school_population / total_population) * 100

        results.append((region, middle_school_ratio))

    # 비율이 가장 높은 지역 찾기
    highest_ratio_region, highest_ratio = max(results, key=lambda x: x[1])

    # 결과 출력
    st.subheader("중학생 비율이 가장 높은 지역")
    st.write(f"지역: {highest_ratio_region}")
    st.write(f"중학생 비율: {highest_ratio:.2f}%")

    # 전체 지역 중 중학생 비율 분포를 시각화
    regions = [result[0] for result in results]
    ratios = [result[1] for result in results]

    fig, ax = plt.subplots()
    ax.barh(regions, ratios, color='#66b3ff')
    ax.set_xlabel('중학생 비율 (%)')
    ax.set_title('각 지역의 중학생 비율')

    st.pyplot(fig)
