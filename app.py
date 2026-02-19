import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. 페이지 설정
st.set_page_config(page_title="기후변화와 생물다양성", layout="wide")

st.title("🌍 기후변화에 따른 생물다양성 변화 대시보드")
st.markdown("""
이 앱은 기온 상승이 지역 생물다양성에 미치는 영향을 시각화합니다. 
왼쪽 사이드바에서 시나리오를 선택해 보세요.
""")

# 2. 가상 데이터 생성 (실제 데이터셋이 있다면 pd.read_csv 사용)
def load_data():
    years = np.arange(2000, 2026)
    temp_increase = np.linspace(0, 2.5, len(years)) + np.random.normal(0, 0.1, len(years))
    # 기온이 오를수록 개체수는 감소하는 경향성 반영
    species_a = 1000 - (temp_increase * 200) + np.random.normal(0, 30, len(years))
    species_b = 800 - (temp_increase * 100) + np.random.normal(0, 20, len(years))
    
    df = pd.DataFrame({
        '연도': years,
        '평균기온편차(°C)': temp_increase,
        'A종 개체수': species_a,
        'B종 개체수': species_b
    })
    return df

df = load_data()

# 3. 사이드바 - 필터링
st.sidebar.header("📊 필터 및 설정")
selected_species = st.sidebar.multiselect(
    "관찰할 종 선택", 
    ['A종 개체수', 'B종 개체수'], 
    default=['A종 개체수']
)

# 4. 메인 화면 - 시각화
col1, col2 = st.columns(2)

with col1:
    st.subheader("🌡️ 연도별 기온 변화")
    fig_temp = px.line(df, x='연도', y='평균기온편차(°C)', 
                       title="지구 온난화 추이", markers=True)
    st.plotly_chart(fig_temp, use_container_width=True)

with col2:
    st.subheader("🦋 생물 개체수 변화")
    fig_species = px.line(df, x='연도', y=selected_species, 
                          title="선택한 종의 개체수 변화")
    st.plotly_chart(fig_species, use_container_width=True)

# 5. 상관관계 분석
st.divider()
st.subheader("🔍 기온과 생물 개체수의 상관관계")
# 상관관계를 보여주는 산점도
fig_corr = px.scatter(df, x='평균기온편차(°C)', y=selected_species[0] if selected_species else 'A종 개체수',
                     trendline="ols", title="기온 상승에 따른 개체수 감소 분석")
st.plotly_chart(fig_corr, use_container_width=True)

st.info("💡 **분석 결과:** 기온이 상승할수록 관찰되는 생물 종의 개체수가 급격히 감소하는 음의 상관관계를 보입니다.")
