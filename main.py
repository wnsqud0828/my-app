import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import rcParams

# 한글 폰트 설정
matplotlib.rcParams['font.family'] = 'NanumGothic'
matplotlib.rcParams['axes.unicode_minus'] = False

# 제목 및 파일 업로드
st.title("연령대 비율 비교 분석")
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요:", type="csv")

if uploaded_file is not None:
    # 데이터 읽기
    try:
        data = pd.read_csv(uploaded_file, encoding='euc-kr')
    except Exception as e:
        st.error(f"파일을 읽어오는 중 오류가 발생했습니다: {e}")
        st.stop()

    # 연령대 설정 (0~9세, 10~19세, ... , 90~99세, 100세 이상)
    age_groups = {
        '0대': [f"2024년06월_계_{age}세" for age in range(0, 10)],
        '10대': [f"2024년06월_계_{age}세" for age in range(10, 20)],
        '20대': [f"2024년06월_계_{age}세" for age in range(20, 30)],
        '30대': [f"2024년06월_계_{age}세" for age in range(30, 40)],
        '40대': [f"2024년06월_계_{age}세" for age in range(40, 50)],
        '50대': [f"2024년06월_계_{age}세" for age in range(50, 60)],
        '60대': [f"2024년06월_계_{age}세" for age in range(60, 70)],
        '70대': [f"2024년06월_계_{age}세" for age in range(70, 80)],
        '80대': [f"2024년06월_계_{age}세" for age in range(80, 90)],
        '90대': [f"2024년06월_계_{age}세" for age in range(90, 100)],
        '100세 이상': [f"2024년06월_계_{age}세" for age in range(100, 110)]
    }

    # 도시 리스트 및 비율 계산
    cities = []
    ratios = {}

    # 연령대 선택
    selected_age_group = st.selectbox("비율을 구할 연령대를 선택하세요:", list(age_groups.keys()))

    for _, row in data.iterrows():
        region = row.get('행정구역', '')

        # 선택한 연령대의 인구수 합계 계산
        age_columns = age_groups.get(selected_age_group, [])
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
        selected_ratio = ratios.get(selected_city, 0)

        # 비율이 가장 비슷한 도시 찾기
        differences = {city: abs(ratio - selected_ratio) for city, ratio in ratios.items() if city != selected_city}
        if differences:
            similar_city = min(differences, key=differences.get)
            similar_ratio = ratios.get(similar_city, 0)

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
        else:
            st.write("비슷한 비율을 가진 도시가 없습니다.")
