import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib

file_path = '202406_202406_연령별인구현황_월간 (2).csv'
data = pd.read_csv(file_path, encoding='euc-kr')

middle_school_ages = ['2024년06월_계_12세', '2024년06월_계_13세', '2024년06월_계_14세']

st.title("중학생 연령대 인구 비율")
selected_region = st.selectbox('지역을 선택하세요:', data['행정구역'].unique())


region_data = data[data['행정구역'] == selected_region]


middle_school_population = region_data[middle_school_ages].apply(lambda x: x.str.replace(',', '').astype(int)).sum(axis=1).values[0]


total_population = int(region_data['2024년06월_계_총인구수'].str.replace(',', '').values[0])

middle_school_ratio = (middle_school_population / total_population) * 100


labels = ['중학생 연령대', '기타 연령대']
sizes = [middle_school_ratio, 100 - middle_school_ratio]
colors = ['#ff9999','#66b3ff']
explode = (0.1, 0)

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
        shadow=True, startangle=140)
ax1.axis('equal')


st.pyplot(fig1)
