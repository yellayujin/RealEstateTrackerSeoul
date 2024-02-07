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
                 hole=0.4,
                 )

    fig.update_traces(textposition='inside', textinfo='percent+label', pull = [0, 0,0, 0, 0, 0, 0.1])  
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
        st.header('🔎지역 검색')
        st.subheader('선택한 지역의 실거래 데이터를 분석해드립니다!')
        # 구 선택
        sgg_nm_sort=sorted(df['SGG_NM'].unique())
        selected_sgg_nm = st.selectbox(
            '자치구를 선택하세요.',
            options=list(sgg_nm_sort), index = None
        )   

        # 동 선택(조건: 선택된 구 안에 있는 동을 보여줘야 함)
        selected_bjdong_nm = st.selectbox('법정동을 선택하세요', 
                                            options= sorted(df.loc[df['SGG_NM']==selected_sgg_nm, :].BJDONG_NM.unique()), index=None)
        st.divider()
        
        # 홈 화면 버튼


        # 언어 선택
        # st.subheader('Language')
        # lang = st.radio('Select Your Language', ['English', 'Korean'], index = 1)
        # if lang == 'English':
        #    st.page_link('https://yellayujin-miniproject2-app-eng-aapmoa.streamlit.app/', label = 'Click here to explore in English')  

        # st.divider()



    # 출력하고자 하는 데이터 선택
    filtered_data = df.loc[(df['SGG_NM'] == selected_sgg_nm)&(df['BJDONG_NM']==selected_bjdong_nm)]


    if selected_bjdong_nm == None:
        # 여백 추가를 위한 스타일 지정
        main_style = """
            padding : 10px;
            margin: 50px;
            """

        st.title('부동산 트래커: 서울')
        st.markdown('서울시 전체 부동산 거래량 및 통계 정보를 얻을 때, 지역별 부동산 유형에 따른 거래 동향을 알아보고 싶을 때 부동산 트래커를 통해 확인하세요!')


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


        # 각 건물용도별 최대값 및 최소값 초기화
        values = {
            '아파트': {'max_amount': None, 'min_amount': None, 'max_location': None, 'min_location': None, 'max_building': None, 'min_building': None},
            '오피스텔': {'max_amount': None, 'min_amount': None, 'max_location': None, 'min_location': None, 'max_building': None, 'min_building': None},
            '연립다세대': {'max_amount': None, 'min_amount': None, 'max_location': None, 'min_location': None, 'max_building': None, 'min_building': None},
            '단독다가구': {'max_amount': None, 'min_amount': None, 'max_location': None, 'min_location': None, 'max_building': None, 'min_building': None}
        }

        for house_type in ['아파트', '오피스텔', '연립다세대','단독다가구']:
            # 해당 건물용도의 데이터 필터링
            filtered_data = df[df['HOUSE_TYPE'] == house_type]
            
            # 거래금액('OBJ_AMT') 열에서 최대 값 및 최소 값 찾기
            max_amount = filtered_data['OBJ_AMT'].max()
            min_amount = filtered_data['OBJ_AMT'].min()
            
            # 최대값 및 최소값을 가진 행 찾기
            max_row = filtered_data[filtered_data['OBJ_AMT'] == max_amount].iloc[0]
            min_row = filtered_data[filtered_data['OBJ_AMT'] == min_amount].iloc[0]

            # 최대값 및 최소값 및 위치 정보 저장
            values[house_type]['max_amount'] = max_amount
            values[house_type]['min_amount'] = min_amount
            values[house_type]['max_location'] = max_row['SGG_NM'] if not pd.isna(max_row['SGG_NM']) else ''
            values[house_type]['max_location'] += ' ' + max_row['BJDONG_NM'] if not pd.isna(max_row['BJDONG_NM']) else ''
            values[house_type]['max_building'] = max_row['BLDG_NM'] if not pd.isna(max_row['BLDG_NM']) else ''
            values[house_type]['min_location'] = min_row['SGG_NM'] if not pd.isna(min_row['SGG_NM']) else ''
            values[house_type]['min_location'] += ' ' + min_row['BJDONG_NM'] if not pd.isna(min_row['BJDONG_NM']) else ''
            values[house_type]['min_building'] = min_row['BLDG_NM'] if not pd.isna(min_row['BLDG_NM']) else ''


        st.subheader("서울시 건물용도별 최고가/최소가 정보")

        # 칸 생성
        col5, col6, col7, col8 = st.columns(4)

        # 칸에 내용 추가
        with col5:
            st.markdown(f'<div style = "height: 220px; border: 1px solid white; padding: 10px; box-shadow: 2px,2px,5px rgba(0,0,0,0.1); "><h6 style="text-align: center; color: gray;">아파트</h6><h5 style="text-align: center; color: blue;">최고가</h5><h5 style = "text-align: center;">{values["아파트"]["max_amount"]:,.0f}만원<h5><h6>{values["아파트"]["max_location"]}<br>{values["아파트"]["max_building"]}</h6></div>', unsafe_allow_html=True)
        with col6:
            st.markdown(f'<div style = "height: 220px; border: 1px solid white; padding: 10px; box-shadow: 2px,2px,5px rgba(0,0,0,0.1); "><h6 style="text-align: center; color: gray;">오피스텔</h6><h5 style="text-align: center; color: blue;">최고가</h5><h5 style = "text-align: center;">{values["오피스텔"]["max_amount"]:,.0f}만원<h5><h6>{values["오피스텔"]["max_location"]}<br>{values["오피스텔"]["max_building"]}</h6></div>', unsafe_allow_html=True)  
        with col7:
            st.markdown(f'<div style = "height: 220px; border: 1px solid white; padding: 10px; box-shadow: 2px,2px,5px rgba(0,0,0,0.1); "><h6 style="text-align: center; color: gray;">연립다세대</h6><h5 style="text-align: center; color: blue;">최고가</h5><h5 style = "text-align: center;">{values["연립다세대"]["max_amount"]:,.0f}만원<h5><h6>{values["연립다세대"]["max_location"]}<br>{values["연립다세대"]["max_building"]}</h6></div>', unsafe_allow_html=True)
        with col8:
            st.markdown(f'<div style = "height: 220px; border: 1px solid white; padding: 10px; box-shadow: 2px,2px,5px rgba(0,0,0,0.1); "><h6 style="text-align: center; color: gray;">단독다가구</h6><h5 style="text-align: center; color: blue;">최고가</h5><h5 style = "text-align: center;">{values["단독다가구"]["max_amount"]:,.0f}만원<h5><h6>{values["단독다가구"]["max_location"]}<br>{values["단독다가구"]["max_building"]}</h6></div>', unsafe_allow_html=True)
        

        st.markdown("")


        # 칸 생성
        col9, col10, col11, col12 = st.columns(4)

        with col9:
            st.markdown(f'<div style = "height: 220px; border: 1px solid white; padding: 10px; box-shadow: 2px,2px,5px rgba(0,0,0,0.1); "><h6 style="text-align: center; color: gray;">아파트</h6><h5 style="text-align: center; color: red;">최저가</h5><h5 style = "text-align: center;">{values["아파트"]["min_amount"]:,.0f}만원<h5><h6>{values["아파트"]["min_location"]}<br>{values["아파트"]["min_building"]}</h6></div>', unsafe_allow_html=True)
        with col10:
            st.markdown(f'<div style = "height: 220px; border: 1px solid white; padding: 10px; box-shadow: 2px,2px,5px rgba(0,0,0,0.1); "><h6 style="text-align: center; color: gray;">오피스텔</h6><h5 style="text-align: center; color: red;">최저가</h5><h5 style = "text-align: center;">{values["오피스텔"]["min_amount"]:,.0f}만원<h5><h6>{values["오피스텔"]["min_location"]}<br>{values["오피스텔"]["min_building"]}</h6></div>', unsafe_allow_html=True)
        with col11:
            st.markdown(f'<div style = "height: 220px; border: 1px solid white; padding: 10px; box-shadow: 2px,2px,5px rgba(0,0,0,0.1); "><h6 style="text-align: center; color: gray;">연립다세대</h6><h5 style="text-align: center; color: red;">최저가</h5><h5 style = "text-align: center;">{values["연립다세대"]["min_amount"]:,.0f}만원<h5><h6>{values["연립다세대"]["min_location"]}<br>{values["연립다세대"]["min_building"]}</h6></div>', unsafe_allow_html=True)
        with col12:
            st.markdown(f'<div style = "height: 220px; border: 1px solid white; padding: 10px; box-shadow: 2px,2px,5px rgba(0,0,0,0.1); "><h6 style="text-align: center; color: gray;">단독다가구</h6><h5 style="text-align: center; color: red;">최저가</h5><h5 style = "text-align: center;">{values["단독다가구"]["min_amount"]:,.0f}만원<h5><h6>{values["단독다가구"]["min_location"]}<br>{values["단독다가구"]["min_building"]}</h6></div>', unsafe_allow_html=True)
        


    # 지역 골랐을 때 페이지 출력되게
    if selected_bjdong_nm != None:
        st.header('서울시 부동산 트래커')
        tab1, tab2, tab3 = st.tabs(["한눈에 보기", "키워드 상세 조회", "타 법정동 비교"])
        with tab1:
            st.subheader('거래 금액')
            st.markdown(f'{selected_sgg_nm} {selected_bjdong_nm}의 거래금액을 서울시 전체의 매매건과 비교하여 보여드립니다!')
            
            # round(filtered_data.OBJ_AMT.mean(), 1)
            # '{0:,}'.format(round(filtered_data.OBJ_AMT.mean(), 1))
            col1, col2, col3 = st.columns(3)
            with col1: 
                st.metric(label = '평균(만 원)', value = '{0:,}'.format(round(filtered_data.OBJ_AMT.mean(), 1)), delta = '{0:,}'.format(round(filtered_data.OBJ_AMT.mean() - df.OBJ_AMT.mean(), 1)))
            with col2: 
                st.metric(label = '최대(만 원)', value = '{0:,}'.format(round(filtered_data.OBJ_AMT.max(), 1)), delta = str('{0:,}'.format(round(filtered_data.OBJ_AMT.max() - df.OBJ_AMT.max(), 1))))
            with col3: 
                st.metric(label = '최소(만 원)', value = '{0:,}'.format(round(filtered_data.OBJ_AMT.min(), 1)), delta = str('{0:,}'.format(round(filtered_data.OBJ_AMT.min() - df.OBJ_AMT.min(), 1))))

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
            options_dict = {'물건금액대':'OBJ_AMT_LV', '건물유형':'HOUSE_TYPE', '지번구분명':'LAND_GBN_NM', '거래연도':'DEAL_YMD', '건축연도':'BUILD_YEAR'}
            
            st.write(f'{selected_sgg_nm} {selected_bjdong_nm}의 실거래건 중 관심있는 정보를 확인하세요!')
            filtered_data['OBJ_AMT_LV'] = pd.cut(filtered_data['OBJ_AMT'], bins = [0, 10000, 50000, 100000, 150000, 200000, 3000000], labels = ['1억 미만','1억~5억', '5억~10억', '10억~20억', '20억~25억', '25억 이상'], include_lowest=True)
            filtered_data['DEAL_YMD'] = filtered_data['DEAL_YMD'].dt.year
            filtered_data['BUILD_YEAR'] = np.where(filtered_data['BUILD_YEAR']==np.nan, 0, filtered_data['BUILD_YEAR'])
            filtered_data = filtered_data.astype({'BUILD_YEAR':'str', 'DEAL_YMD':'str'})    
            filtered_data['BUILD_YEAR'] = filtered_data['BUILD_YEAR'].str[:4]
            options = st.selectbox(
                '관심 키워드를 선택하세요.', options_dict.keys(), index=None)
                # ['물건금액대', '건물유형', '지번구분명', '거래연도', '건축일']
            

            if options != None:
                st.divider()
                st.subheader('키워드 검색 결과')
                st.caption('각 탭을 누르면 오름차순(내림차순) 확인이 가능합니다.')
                col = []
                key = options
                colname = options_dict[key]
                col.append(options_dict[key])
                table = pd.DataFrame(filtered_data.groupby(by = colname, observed=True))

                unique = []
                for i in table.iloc[:,0]:
                    # st.write(f'{i}')
                    unique.append(i)
                selected_unique = st.radio('조회할 유형 선택', unique)
                st.write('유형 별 요약정보')
                st.write(filtered_data[filtered_data[colname] == selected_unique].describe().T)

                st.write(f'유형 별 전체 데이터 조회')
                # selected_unique = st.radio('조회할 유형 선택', unique)
                if selected_unique == '단독다가구':
                    st.caption('Note: 단독 다가구의 경우 본번, 부번과 같은 상세정보는 제공되지 않습니다.')
                st.write(filtered_data[filtered_data[colname] == selected_unique])
                st.divider()
                
                # st.write(filtered_data[col])                 # groupby로 뭔가 될 듯 한데...
            # filtered_data = filtered_data.astype({'BUILD_YEAR':'int'})           
            
                    

        with tab3:
            # st.header('상세 검색')
            st.write(f'{selected_sgg_nm} 내 다른 동과 거래 내용을 비교하세요!')
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
                floor=st.number_input('층수를 입력하세요',step=1,min_value=-1,max_value=68, value = 1)
                pyeong=st.number_input('평수를 입력하세요',step=1, value = 25)
                buildyear=st.number_input('건축연도를 입력하세요',step=1, value = 2010)
                alpha=st.slider('오차범위를 선택하세요',0,10,2)
                
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
                                        zoom=9.4,
                                        center={"lat": 37.5650172, "lon": 126.9782914},
                                        opacity=0.5,
                                        labels={'Avg_Obj_Amt': '평균 거래액'},
                                        hover_data={'SGG_NM': True, 'Avg_Obj_Amt': True}
                                        )
                st.plotly_chart(fig)
                     
            else:        
                values = st.slider(
                    '건물 가격 범위를 설정하세요.',
                    1000.0, 3000000.0, (10000.0, 300000.0))
                st.write('가격 범위:', values)

                # 금액대 설정 후 같은 구 내에서 다른 동 정보
                df = df.astype({'BUILD_YEAR':'str'})    
                df['BUILD_YEAR'] = df['BUILD_YEAR'].str.rstrip('.0')
                others = df.loc[(df.SGG_NM == selected_sgg_nm) & (df.BJDONG_NM != selected_bjdong_nm), :]
                others['DEAL_YMD'] = others['DEAL_YMD'].dt.date
                st.write(others.loc[(values[0] <= others.OBJ_AMT) & (others.OBJ_AMT <= values[1]),:])



        




if __name__ == "__main__":
    main()