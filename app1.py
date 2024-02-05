# -*- coding:utf-8 -*-
# 19년, 24년(양 끝 연도) 제거해야함

import streamlit as st 
import pandas as pd
from data_collect import load_data
from data_collect import Range   # 한울님 감사합니다!
from data_collect import load_geojsondata   
import plotly.express as px 
import plotly.graph_objects as go 
from datetime import datetime

# 큰 구현 내용
 # 첫 화면
 # 자치구, 법정동 고르면 첫 화면 사라지고 분석 내용 나오게
  # 서울시 전체 거래 건과 비교한 거래 금액(평균, 최대, 최소), (연도 선택 후 월별)거래 건수, 건물 용도

# 사이드바
 # 자치구, 법정동 선택
   # 자치구 고르면 그 구에 해당되는 법정동만 고를 수 있게
 # 언어 선택 후 해당 페이지로 이동하게
 # 홈 화면으로

def main():
    
    df=load_data()

    # 사이드바
    # 코드로 데이터 검색?
    with st.sidebar:
        st.header('Filter')
        st.subheader('선택한 지역의 실거래 데이터를 분석해드립니다!')
        # 구 선택
        selected_sgg_nm = st.selectbox('자치구명', options= df['SGG_NM'].unique(), index=None, placeholder='구를 선택하세요.')

        # 동 선택(조건: 선택된 구 안에 있는 동을 보여줘야 함)
        selected_bjdong_nm = st.selectbox('법정동명', 
                                            options= df.loc[df['SGG_NM']==selected_sgg_nm, :].BJDONG_NM.unique())
        st.divider()
        
        # 언어 선택
        st.subheader('Language')
        lang = st.radio('Select Your Language', ['English', 'Korean'], index = 1)
        if lang == 'English':
            st.page_link('app1.py', label = 'Click here to explore in English')
        elif lang == 'Korean':
            st.page_link('app1.py', label='Click here to explore in Korean')    # ???
                

        st.divider()

        # 홈 화면 버튼
        if st.button('🏠첫 화면으로'):
            st.stop()
            st.rerun()

    # 출력하고자 하는 데이터 선택
    filtered_data = df.loc[(df['SGG_NM'] == selected_sgg_nm)&(df['BJDONG_NM']==selected_bjdong_nm)]

    if selected_bjdong_nm == None:
        st.title('Customed Searching Service for Foreigners')
        st.subheader('Subheader')
        st.markdown('Welcome! 대시보드 제공 대상 및 목적 & 아래에 Overview 제공')
        st.write('Overview of Deal in Seoul') # Overview를 첫 tab에 넣을....아니다 구분하자

    # 지역 골랐을 때 페이지 출력되게
    if selected_bjdong_nm != None:
        tab1, tab2, tab3 = st.tabs(["Overview", "상세 조회", "tab3"])
        with tab1:
            st.subheader('거래 금액')
            st.markdown('선택한 지역의 거래금액을 서울시 전체의 매매건과 비교하여 보여드립니다!')
            
            col1, col2, col3 = st.columns(3)
            with col1: 
                st.metric(label = '평균(만 원)', value = round(filtered_data.OBJ_AMT.mean(), 1), delta = round(filtered_data.OBJ_AMT.mean() - df.OBJ_AMT.mean(), 1))
            with col2: 
                st.metric(label = '최대(만 원)', value = round(filtered_data.OBJ_AMT.max(), 1), delta = str(round(filtered_data.OBJ_AMT.max() - df.OBJ_AMT.max(), 1)))
            with col3: 
                st.metric(label = '최소(만 원)', value = round(filtered_data.OBJ_AMT.min(), 1), delta = str(round(filtered_data.OBJ_AMT.min() - df.OBJ_AMT.min(), 1)))

            st.divider()
            st.subheader('거래 건수') 
            # 2020, 21, 22, 23년도의 거래 건수 추이 비교??

            # 거래 일자를 날짜형으로
            filtered_data['DEAL_YMD_dt'] = pd.to_datetime(filtered_data['DEAL_YMD'], format='ISO8601')  

            # 연도별 거래량-> 각 연도별 그래프 하나로 합치는 것도 좋을듯
            year = st.radio("연도를 고르세요.", ['2020', '2021', '2022', '2023'])
            filtered_data_year = filtered_data.loc[filtered_data['DEAL_YMD_dt'].dt.year == int(year), :]
            st.line_chart(filtered_data_year['DEAL_YMD_dt'].dt.month_name().value_counts())   


            # 건물 용도
            st.subheader('건물 용도')
            st.bar_chart(filtered_data['HOUSE_TYPE'].value_counts())




        with tab2:
            st.header('상세한 검색 조건')
            st.write('세부 옵션을 설정하세요.')







if __name__ == "__main__":
    main()