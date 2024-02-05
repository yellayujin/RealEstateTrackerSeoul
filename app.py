# -*- coding:utf-8 -*-

import streamlit as st 
import pandas as pd
from data_collect import load_data
from data_collect import Range
from data_collect import load_geojsondata
import plotly.express as px 
import plotly.graph_objects as go 

def main():
    df=load_data()
    # 대시보드 제목
    st.title('Dashboard Title')

    st.subheader('Subheader')
    # 사용자 입력을 위한 selectbox 생성
    selected_sgg_nm = st.selectbox(
        '구를 선택하세요.',
        options=list(df['SGG_NM'].unique())
    )
    selected_house_type = st.selectbox(
        '용도를 선택하세요.',
        options=list(df['HOUSE_TYPE'].unique())
    )
    
    # 출력하고자 하는 데이터 선택
    filtered_data = df.loc[(df['SGG_NM'] == selected_sgg_nm)&(df['HOUSE_TYPE']==selected_house_type)]
    grouped_data = filtered_data.groupby('BJDONG_NM')['OBJ_AMT'].mean().reset_index()

    # 막대 그래프 그리기
    fig=go.Figure()
    fig.add_trace(
        go.Bar(x=grouped_data.BJDONG_NM,y=grouped_data.OBJ_AMT,
    	    marker={'color':px.colors.qualitative.Dark24,
                        'line':{'color':'black','width':2},
                        'pattern':{'shape':'/'}})    
    )
    fig.update_layout(go.Layout(title={'text':f'{selected_sgg_nm} 법정동별 부동산 평균 거래가격',
                                  'font':{'color':'blue','size':30}},
                            xaxis={'title':{'text':'법정동 이름'},
                                   'gridwidth':1,'showgrid':True},
                            yaxis={'title':{'text':'평균 거래가격(만 원)'},
                                   'gridwidth':1,'showgrid':True},

    ))
    # 그래프 출력
    st.plotly_chart(fig)
    
    st.subheader('평수별 평균 거래가')
    #평수대별로 데이터 나눠서 새로운 컬럼생성
    df['Pyeong']=df['BLDG_AREA']/3.3
    df['Pyeong']=df['Pyeong'].astype('int64')
    df['Pyeong_range']=df['Pyeong'].apply(Range)
    
    # 사용자 입력을 위한 selectbox 생성
    selected_Pyeong = st.selectbox(
        '평수대를 선택하세요.',
        options=list(df['Pyeong_range'].unique())
    )
    st.write(selected_house_type)
    
    # 출력하고자 하는 데이터 선택
    filtered_data = df.loc[(df['Pyeong_range'] == selected_Pyeong)&(df['HOUSE_TYPE']==selected_house_type)]
    grouped_data = filtered_data.groupby('Pyeong')['OBJ_AMT'].mean().reset_index()
    
    # 막대 그래프 그리기
    fig=go.Figure()
    fig.add_trace(
        go.Bar(x=grouped_data.Pyeong,y=grouped_data.OBJ_AMT,
    	    marker={'color':px.colors.qualitative.Dark24,
                        'line':{'color':'black','width':2},
                        'pattern':{'shape':'/'}})    
    )
    fig.update_layout(go.Layout(title={'text':f'{selected_Pyeong} 부동산 평균 거래가격',
                                  'font':{'color':'blue','size':30}},
                            xaxis={'title':{'text':'평수대'},
                                   'gridwidth':1,'showgrid':True},
                            yaxis={'title':{'text':'평균 거래가격(만 원)'},
                                   'gridwidth':1,'showgrid':True},

    ))
    # 그래프 출력
    st.plotly_chart(fig)
    
    st.subheader('시간별 거래가격의 변화')
    st.write(selected_house_type)
    # 날짜 형식을 올바르게 지정하여 datetime으로 변환
    df['YearMonth'] = pd.to_datetime(df['DEAL_YMD'].astype(str).str.slice(0, 6), format='%Y%m').dt.strftime('%Y-%m')

    # 년월 별 OBJ_AMT 평균 계산
    filtered_data=df.loc[df['HOUSE_TYPE']==selected_house_type]
    monthly_avg_obj_amt = filtered_data.groupby('YearMonth')['OBJ_AMT'].mean().reset_index()

    # 선 그래프로 시각화: x축 정보를 'YYYY-MM' 형식으로 표시
    fig=go.Figure()
    fig.add_trace(
        go.Scatter(x=monthly_avg_obj_amt.YearMonth,y=monthly_avg_obj_amt.OBJ_AMT,mode='lines+markers',line_shape='spline')
    )
    fig.update_traces(line_color='blue',
                    line_width=2,
                    )
    
    fig.update_layout(go.Layout(title={'text':f'시간별 거래가격의 변화',
                                  'font':{'color':'blue','size':30}},
                            xaxis={'title':{'text':'시기'},
                                   'gridwidth':1,'showgrid':True},
                            yaxis={'title':{'text':'평균 거래가격(만 원)'},
                                   'gridwidth':1,'showgrid':True},))

    st.plotly_chart(fig)
    
    st.subheader('매물 검색기')
    
    show_list=['BJDONG_NM','BONBEON','BUBEON','BLDG_NM','OBJ_AMT','BLDG_AREA','FLOOR']
    selected_multi_sgg_nm = st.multiselect(
        '구를 선택하세요.',
        options=list(df['SGG_NM'].unique())
    )
    selected_multi_house_type = st.multiselect(
        '용도를 선택하세요.',
        options=list(df['HOUSE_TYPE'].unique())
    )
    selected_multi_Pyeong = st.multiselect(
        '평수대를 선택하세요.',
        options=list(df['Pyeong_range'].unique())
    )
    
    filtered_data=df.loc[(df['SGG_NM'].isin(selected_multi_sgg_nm))
                         &(df['HOUSE_TYPE'].isin(selected_multi_house_type))
                         &(df['Pyeong_range'].isin(selected_multi_Pyeong)),
                         show_list]
    st.data_editor(filtered_data.head())
    
    st.subheader('gis 시각화')
    #geojson 파일 불러오기
    gdf=load_geojsondata()
    #df에서 SGG_NM 빈도수 계산
    sgg_nm_counts = df['SGG_NM'].value_counts().reset_index()
    sgg_nm_counts.columns = ['SIG_KOR_NM', 'Counts']
    #geojson과 데이터프레임 병합
    merged_gdf = gdf.merge(sgg_nm_counts, on='SIG_KOR_NM')
    
    #시각화
    fig = px.choropleth_mapbox(merged_gdf,
                           geojson=merged_gdf.geometry.__geo_interface__,
                           locations=merged_gdf.index,
                           color='Counts',
                           color_continuous_scale="Viridis",
                           mapbox_style="carto-positron",
                           zoom=10,
                           center={"lat": 37.5650172, "lon": 126.9782914},
                           opacity=0.5,
                           labels={'Counts':'빈도수'},
                           hover_data={'SIG_KOR_NM': True, 'Counts': True}
                          )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig)
    
    
if __name__ == "__main__":
    main()
    