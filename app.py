# -*- coding:utf-8 -*-

import streamlit as st 
import pandas as pd
import numpy as np
from data_collect import load_data
from data_collect import Range  
from data_collect import load_geojsondata   
import plotly.express as px 
import plotly.graph_objects as go 
from datetime import datetime
import requests
from io import StringIO


def load_deals_by_month(df, year, month):
    # 지정한 년도와 월에 해당하는 거래 데이터를 불러옴
    target_month = f'{year}-{month:02d}'
    deals = df[df['DEAL_YMD'].dt.to_period('M') == pd.Period(target_month, freq = 'M')]
    deals['count'] = 1 # count열 추가
    deal_count = deals.shape[0]
    return deals, deal_count

def find_highest_increase_area(df, current_month,comparison_month ):
    # 기준 월에 해당하는 거래 데이터를 불러옴
    current_month_deals, current_month_deal_count = load_deals_by_month(df, *current_month)

    # 비교 월에 해당하는 거래 데이터를 불러옴
    comparison_month_deals, comparison_month_deal_count = load_deals_by_month(df, *comparison_month)

    # 기준 월과 비교 월의 거래량 계산
    current_month_deal_counts = current_month_deals['SGG_NM'].value_counts()
    comparison_month_deal_counts = comparison_month_deals['SGG_NM'].value_counts()

    # 거래량 증가율 계산
    increase_rates = (current_month_deal_counts - comparison_month_deal_counts)/comparison_month_deal_counts * 100

    # 증가율이 가장 높은 자치구 찾기
    highest_increase_area = increase_rates.idxmax()
    highest_increase_rate = round(increase_rates.max(), 1)

    return highest_increase_area, highest_increase_rate

def find_most_active_area(deals):
    # 거래량이 가장 많은 자치구 찾기
    most_active_area = deals['SGG_NM'].value_counts().idxmax()
    most_active_count = deals['SGG_NM'].value_counts().max()
    return most_active_area, most_active_count

def find_highest_avg_amt_area(df, year, month):
    # 지정한 년도와 월에 해당하는 거래 데이터를 불러옴
    target_month = f'{year}-{month:02d}'
    deals = df[df['DEAL_YMD'].dt.to_period('M') == pd.Period(target_month, freq = 'M')]

    # 자치구별로 OGJ_AMT의 평균 계산
    avg_amt_by_area = deals.groupby('SGG_NM')['OBJ_AMT'].mean()

    # 가장 높은 평균값을 가진 자치구 찾기
    highest_avg_amt_area = avg_amt_by_area.idxmax()
    highest_avg_amt_value = avg_amt_by_area.max()

    return highest_avg_amt_area, highest_avg_amt_value

def get_darker_color(color, factor=0.7):
    r, g, b = [int(color[i:i+2], 16) for i in (1, 3, 5)]
    r = max(0, int(r * factor))
    g = max(0, int(g * factor))
    b = max(0, int(b * factor))
    return f"#{r:02x}{g:02x}{b:02x}"

def plot_pie_chart(deals):
    colors = px.colors.sequential.Blues

    fig = px.pie(deals, 
                 names='SGG_NM', 
                 title='2023년 05월 서울시 자치구별 거래 비율',
                 color='SGG_NM',
                 color_discrete_sequence=colors,
                 labels={'SGG_NM': '자치구명'},
                 hole=0.3,
                 )

    fig.update_traces(textposition='inside', textinfo='percent+label', pull=[0.1, 0.1, 0.1, 0.1])  
    fig.update_layout(
        showlegend=False,  
        margin=dict(l=0, r=0, b=0, t=30),  
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)',  
    )

    st.plotly_chart(fig, use_container_width=True)


def plot_bar_chart(deals):
    fig = px.bar(deals, x = 'HOUSE_TYPE', title = '2023년 05월 부동산 거래 유형별 거래 건수', labels = {'HOUSE_TYPE': '부동산 유형', 'count': '거래 건수'})
    fig.update_layout(xaxis_title = '부동산 유형', yaxis_title = '거래 건수')
    st.plotly_chart(fig, use_container_width= True)




def main():
    
    df=load_data()
    df['DEAL_YMD'] = pd.to_datetime(df['DEAL_YMD'], format = '%Y%m%d')  # 날짜형 변환
    df['CNTL_YMD'] = pd.to_datetime(df['CNTL_YMD'], format = '%Y%m%d').dt.date
    df = df.astype({'ACC_YEAR': 'str', 'BONBEON': 'str', 'BUBEON': 'str'})  # 본번, 부번은 끝에 .0붙음(결측 때문?), 건축연도는 후에 계산(tab3, line 263)때문에 잠깐 패스
    
    df['BONBEON'] = df['BONBEON'].str.rstrip('.0')
    df['BUBEON'] = df['BUBEON'].str.rstrip('.0')

    # 사이드바
    with st.sidebar:
        st.header('지역 검색')
        st.subheader('선택한 지역의 실거래 데이터를 분석해드립니다!')
        # 구 선택
        sgg_nm_sort=sorted(df['SGG_NM'].unique())
        selected_sgg_nm = st.selectbox(
            '구를 선택하세요.',
            options=list(sgg_nm_sort)
        )   

        # 동 선택(조건: 선택된 구 안에 있는 동을 보여줘야 함)
        selected_bjdong_nm = st.selectbox('법정동명', 
                                            options= sorted(df.loc[df['SGG_NM']==selected_sgg_nm, :].BJDONG_NM.unique()))
        st.divider()
        
        # 홈 화면 버튼

        
        # 언어 선택
        st.subheader('Language')
        lang = st.radio('Select Your Language', ['English', 'Korean'], index = 1)
        if lang == 'English':
            st.page_link('https://yellayujin-miniproject2-app-eng-aapmoa.streamlit.app/', label = 'Click here to explore in English')  

        st.divider()


    # 출력하고자 하는 데이터 선택
    filtered_data = df.loc[(df['SGG_NM'] == selected_sgg_nm)&(df['BJDONG_NM']==selected_bjdong_nm)]


    if selected_bjdong_nm == None:
        # 여백 추가를 위한 스타일 지정
        main_style = """
            padding : 10px;
            margin: 50px;
            """

        st.title('부동산 트랙커: 서울')
        st.markdown('서울시 전체 부동산 거래량 및 통계 정보를 얻을 때, 지역별 부동산 유형에 따른 거래 동향을 알아보고 싶을 때 부동산 트랙커를 통해 확인하세요.')


        # 2023년 05월 거래량 계산
        may_2023_deals, may_2023_deal_count = load_deals_by_month(df,2023,5)

        # 현재 월과 비교할 월 지정
        current_month = {2023, 5}
        comparison_month = {2023, 4}

        # 거래량이 가장 많은 자치구 찾기
        most_active_area, most_active_count = find_most_active_area(may_2023_deals)

        # 거래량 증가율이 가장 높은 자치구 찾기
        highest_increase_area, highest_increase_rate = find_highest_increase_area(df, current_month, comparison_month)

        # 가장 높은 평균 거래 가격을 가진 자치구 찾기
        highest_avg_amt_area, highest_avg_amt_value = find_highest_avg_amt_area(may_2023_deals, 2023, 5)


        # 네 개의 칸을 만들기
        col1, col2, col3, col4 = st.columns(4)
    
        # 각각의 칸에 내용 추가
        st.caption('2023년 05월 기준')
        with col1 :
            st.markdown(f'<div style = "border : 1px solid white; padding: 10px; box-shadow: 2px,2px,5px rgba(0,0,0,0.1); "><h6>서울시 전체 거래량</h6><br><br><h3 style = "text-align: center;">{may_2023_deal_count}건</h3><br></div>', unsafe_allow_html=True)
        with col2 :
            st.markdown(f'<div style = "border : 1px solid white; padding: 10px; box-shadow : 2px,2px,5px rgba(0,0,0,0.1);"><h6>거래량이 가장 많이<br>증가한 자치구</h6><br><h3 style = "text-align: center;">{highest_increase_area}<br><p style ="text-align: right;">({highest_increase_rate}% 증가)</div>', unsafe_allow_html=True)
        with col3 :
            st.markdown(f'<div style = "border : 1px solid white; padding: 10px; box-shadow : 2px,2px,5px rgba(0,0,0,0.1);"><h6>거래량이 가장<br>많은 자치구</h6><br><h3 style = "text-align: center;">{most_active_area}<br><p style ="text-align: right;">({most_active_count}건 증가)</div>', unsafe_allow_html=True)
        with col4 :
            st.markdown(f'<div style = "border : 1px solid white; padding: 10px; box-shadow : 2px,2px,5px rgba(0,0,0,0.1);">'
                    f'<h6>평균 거래 가격이<br>가장 높은 자치구</h6>'
                    f'<br><h3 style = "text-align : center; ">{highest_avg_amt_area}<br>'
                    f'<p style = "text-align: right; ">({(highest_avg_amt_value*1000): ,.0f} 만원)</div>', unsafe_allow_html = True)

        # pie chart 그리기
        plot_pie_chart(may_2023_deals)

        


    # 지역 골랐을 때 페이지 출력되게
    if selected_bjdong_nm != None:
        tab1, tab2, tab3 = st.tabs(["한눈에 보기", "키워드 상세 조회", "타 법정동 비교"])
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
            st.subheader('월별 거래 건수 추이') 

            # 거래 일자를 날짜형으로
            # filtered_data['DEAL_YMD_dt'] = pd.to_datetime(filtered_data['DEAL_YMD'], format='ISO8601')  

            # 연도별 거래량-> 각 연도별 그래프 하나로 합치는 것도 좋을듯
            year = st.radio("연도를 고르세요.", ['2020', '2021', '2022', '2023'])
            filtered_data_year = filtered_data.loc[filtered_data['DEAL_YMD'].dt.year == int(year), :]
            st.line_chart(filtered_data_year['DEAL_YMD'].dt.month_name().value_counts())   


            # 건물 용도별 거래량
            st.subheader('건물 용도')
            st.bar_chart(filtered_data['HOUSE_TYPE'].value_counts())




        with tab2: 
            options_df = ['OBJ_AMT_LV', 'HOUSE_TYPE', 'LAND_GBN_NM', 'DEAL_YMD', 'BUILD_YMD']
            options_dict = {'물건금액대':'OBJ_AMT', '건물유형':'HOUSE_TYPE', '지번구분명':'LAND_GBN_NM', '거래일':'DEAL_YMD', '건축일':'BUILD_YMD'}
            
            st.write(f'{selected_sgg_nm} {selected_bjdong_nm}의 실거래건 중 관심있는 정보를 확인하세요!')
            filtered_data_year['OBJ_AMT_LV'] = pd.qcut(filtered_data_year['OBJ_AMT'], q = 5, labels = ['낮음', '중간낮음', '중간', '중간높음', '높음'])
            options = st.multiselect(
                '관심 키워드를 선택하세요.', options_dict.keys())
                # ['물건금액대', '건물유형', '지번구분명', '거래일', '건축일']
            

            if len(options) != 0:
                st.divider()
                st.write('키워드 검색 결과')
                st.caption('각 탭을 누르면 오름차순(내림차순) 확인이 가능합니다.')
                col = []
                for key in options:
                    col.append(options_dict[key])
                st.write(filtered_data_year[col])                 # groupby로 뭔가 될 듯 한데...
                    

        with tab3:
            # st.header('상세 검색')
            st.write(f'{selected_sgg_nm} 내 다른 동의 거래 건을 확인하세요!')
            option = st.selectbox('검색 옵션', options = ['건물 정보로 조회','건물 가격으로 조회'] )
            st.divider()

            if option == '건물 정보로 조회':
                st.subheader(option)
                gdf=load_geojsondata()
                df['PYEONG']=df['BLDG_AREA']/3.3
                df['PYEONG']=df['PYEONG'].astype('int64')
                df['Pyeong_range']=df['PYEONG'].apply(Range)
                
                
                selected_house_type = st.selectbox(
                    '용도를 선택하세요.',
                    options=list(df['HOUSE_TYPE'].unique())
                )
                floor=st.number_input('층수를 입력하세요',step=1,min_value=-1,max_value=68)
                pyeong=st.number_input('평수를 입력하세요',step=1)
                buildyear=st.number_input('건축연도를 입력하세요',step=1)
                alpha=st.slider('오차범위를 선택하세요',0,10,1)
                
                filtered_df = df.loc[(df['HOUSE_TYPE']=='아파트')&
                                    ((df['FLOOR'] <= floor+alpha)&(df['FLOOR'] >= floor-alpha))&
                                    ((df['PYEONG'] <= pyeong+alpha)&(df['PYEONG'] >= pyeong-alpha))&
                                    ((df['BUILD_YEAR'] <= buildyear+alpha))&(df['BUILD_YEAR'] >= buildyear-alpha)]
                
                avg_obj_amt = filtered_df.groupby('SGG_NM')['OBJ_AMT'].mean().reset_index()
                avg_obj_amt.columns = ['SGG_NM', 'Avg_Obj_Amt']

                #geojson과 데이터프레임 병합
                merged_gdf = gdf.merge(avg_obj_amt, left_on='SIG_KOR_NM', right_on='SGG_NM')
            
                fig = px.choropleth_mapbox(merged_gdf,
                                        geojson=merged_gdf.geometry.__geo_interface__,
                                        locations=merged_gdf.index,
                                        color='Avg_Obj_Amt',
                                        color_continuous_scale="Viridis",
                                        mapbox_style="carto-positron",
                                        zoom=10,
                                        center={"lat": 37.5650172, "lon": 126.9782914},
                                        opacity=0.5,
                                        labels={'Avg_Obj_Amt': '평균 거래액'},
                                        hover_data={'SGG_NM': True, 'Avg_Obj_Amt': True}
                                        )
                st.plotly_chart(fig)
                     
            else:        
                values = st.slider(
                    '건물 가격 범위를 설정하세요.',
                    1000.0, 3000000.0, (10000.0, 4000.0))
                st.write('가격 범위:', values)

                # 금액대 설정 후 같은 구 내에서 다른 동 정보
                df = df.astype({'BUILD_YEAR':'str'})    
                df['BUILD_YEAR'] = df['BUILD_YEAR'].str.rstrip('.0')
                others = df.loc[(df.SGG_NM == selected_sgg_nm) & (df.BJDONG_NM != selected_bjdong_nm), :]
                others['DEAL_YMD'] = others['DEAL_YMD'].dt.date
                st.write(others.loc[(values[0] <= others.OBJ_AMT) & (others.OBJ_AMT <= values[1]),:])



        




if __name__ == "__main__":
    main()