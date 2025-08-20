import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# layou요소
# columns는 요소를 왼쪽 -> 오른쪽으로 배치할 수 있다.

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
    '오늘의 날씨',
    value='35도'
    )

with col2:
    st.metric(
    '오늘의 미세먼지',
    value='좋음',
    delta='-30',
    delta_color='inverse'
    )
    
with col3:
    st.metric(
    '오늘의 습도',
    value='습함'
    )
    
##
st.markdown('---')

data = {
    '이름' : ['홍길동', '김길동', '박길동'],
    '나이' : [10, 20, 30]
}
df = pd.DataFrame(data)
st.dataframe(df)

st.divider()

st.table(df)

st.json(data)

# datafile.csv > load 로드 > table출력 > px.box() 플롯리 박스 그려서 > st.plotly_chart()

df_abnb = pd.read_csv('./data/ABNB_stock.csv')
st.title('ABNB_stock')
st.table(df_abnb.head(5))

import plotly.express as px
color = px.colors.sequential.Plotly3

df_abnb['YearMonth'] = pd.to_datetime(df_abnb['Date']).dt.to_period('M').astype(str)

fig = px.box(df_abnb, x= 'YearMonth', y='Volume', color="YearMonth", 
    color_discrete_sequence=color)
st.plotly_chart(fig)


###############

st.title('5_9 차트와 이미지 표현')

fig, ax = plt.subplots(figsize=(8, 4))
sns.histplot(df_abnb, x='Volume', ax=ax)


st.pyplot(fig)

x_options = ['Date']
y_options = ['Close', 'Volume']


x_option = st.selectbox(
    'Select X-axis',
    index=None,
    options=x_options
)

y_option = st.selectbox(
    'Select Y-axis',
    index=None,
    options=y_options
)


if x_option and y_option:
    fig3 = px.box(
        data_frame=df_abnb, x=x_option, y=y_option,
        width=500
    )
    st.plotly_chart(fig3)
    
