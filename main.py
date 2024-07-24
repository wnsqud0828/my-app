import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
import koreanize_matplotlib

# 한글 폰트 설정
plt.rc('font', family='Malgun Gothic')

st.title("중학생 연령대 인구 비율")

# 파일 업로드 기능
uploaded_file = st.file_uploader("CSV 파일 업로드", type=["csv"])

if uploaded_file is not None:
    # 업로드된 파일을 DataFrame으로 읽어오기
    try:
        data = pd.read_csv(uploaded_file, encoding='euc-kr')
    except Exception as e:
        st.error(f"파일을 읽어오는 중 오류가 발생했습니다: {e}")
        st.stop()

    # 중학생 연령대 컬럼 선택
    middle_school_ages = ['2024년06월_계_12세', '2024년06월_계_13세', '2024년06월_계_14세']

    selected_region = st.selectbox('지역을 선택하세요:', data['행정구역'].unique())

    region_data = data[data['행정구역'] == selected_region]

    # 선택된 지역에 대한 데이터가 없을 경우 처리
    if region_data.empty:
        st.warning("선택된 지역에 대한 데이터가 없습니다.")
    else:
        try:
            middle_school_population = region_data[middle_school_ages].apply(lambda x: x.str.replace(',', '').astype(int)).sum(axis=1).values[0]
            total_population = int(region_data['2024년06월_계_총인구수'].str.replace(',', '').values[0])

            middle_school_ratio = (middle_school_population / total_population) * 100

            labels = ['중학생 연령대', '기타 연령대']
            sizes = [middle_school_ratio, 100 - middle_school_ratio]
            colors = ['#ff9999', '#66b3ff']
            explode = (0.1, 0)

            fig1, ax1 = plt.subplots()
            ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
                    shadow=True, startangle=140)
            ax1.axis('equal')

            st.pyplot(fig1)

        except Exception as e:
            st.error(f"시각화를 생성하는 중 오류가 발생했습니다: {e}")

