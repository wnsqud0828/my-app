import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import rcParams

# 한글 폰트 설정
matplotlib.rcParams['font.family'] = 'NanumGothic'
matplotlib.rcParams['axes.unicode_minus'] = False

# 파일 업로드
st.title("연령대 비율 비교 분석")
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요:", type="csv")

if uploaded_file is not None:
    # 데이터 읽기
    data = pd.read_csv(uploaded_file, encoding='euc-kr')

    # 연령대 목록 설정
    age_groups = {
        '중학생': ['2024년06월_계_12세', '2024년06월_계_13세', '2024년06월_계_14세'],
        '노인': ['2024년06월_계_65세이상'],
        '50대': ['2024년06월_계_50세', '2024년06월_계_51세', '2024년06월_계_52세', '2024년06월_계_53세', '2024년06월_계_54세', '2024년06월_계_55세'],
        '어린이': ['2024년06월_계_0세', '2024년06월_계_1세', '2024년06월_계_2세', '2024년06월_계_3세', '2024년06월_계_4세', '2024년06월_계_5세', '2024년06월_계_6세', '2024년06월_계_7세', '2024년06월_계_8세', '2024년06월_계_9세', '2024년06월_계_10세', '2024년06월_계_11세']
    }

    # 도시 리스트 및 비율 계산
    cities = []
    ratios = {}
    
    # 연령대 선택
    selected_age_group = st.selectbox("비율을 구할 연령대를 선택하세요:", list(age_groups.keys()))

    for _, row in data.iterrows():
        region = row['행정구역']
        
        # 선택한 연령대의 인구수 합계 계산
        age_columns = age_groups[selected_age_group]
        age_population = 0
        for age_col in age_columns:
            value = row.get(age_col, '0').replace(',', '')
            try:
                age_population += int(value)
            except ValueError:
                continue

        # 총 인구수 계산
        total_population_str = row.get('2024년06월_계_총인구수', '0').replace(',', '')
        try:
            total_population = int(total_population_str)
        except ValueError:
            total_population = 0

        # 비율 계산
        if total_population > 0:
            age_ratio = (age_population / total_population) * 100
        else:
            age_ratio = 0

        cities.append(region)
        ratios[region] = age_ratio

    # 도시 선택
    selected_city = st.selectbox("비교할 도시를 선택하세요:", cities)

    if selected_city:
        selected_ratio = ratios[selected_city]

        # 비율이 가장 비슷한 도시 찾기
        differences = [abs(ratio - selected_ratio) for city, ratio in ratios.items() if city != selected_city]
        similar_city = min(ratios, key=lambda city: abs(ratios[city] - selected_ratio) if city != selected_city else float('inf'))
        similar_ratio = ratios[similar_city]

        # 선택한 도시와 비슷한 도시의 비율 계산
        labels = [f'{selected_age_group} 비율', '기타 비율']
        sizes_selected = [selected_ratio, 100 - selected_ratio]
        sizes_similar = [similar_ratio, 100 - similar_ratio]
        colors = ['#ff9999', '#66b3ff']
        explode = (0.1, 0)

        # 원 그래프 생성
        fig, axs = plt.subplots(1, 2, figsize=(14, 7))

        axs[0].pie(sizes_selected, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
                   shadow=True, startangle=140)
        axs[0].set_title(f"{selected_city} {selected_age_group} 비율")

        axs[1].pie(sizes_similar, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
                   shadow=True, startangle=140)
        axs[1].set_title(f"{similar_city} {selected_age_group} 비율")

        st.pyplot(fig)

        st.write(f"선택한 도시: {selected_city}")
        st.write(f"{selected_age_group} 비율: {selected_ratio:.2f}%")
        st.write(f"가장 비슷한 도시: {similar_city}")
        st.write(f"{selected_age_group} 비율: {similar_ratio:.2f}%")
