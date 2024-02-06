# -*- coding:utf-8 -*-

import streamlit as st  
import pandas as pd
import geopandas as gpd
import plotly.graph_objects as go
import plotly.express as px 
from data_collect import load_data
from data_collect import load_geojsondata
from data_collect import Range

def main():
    df=load_data()

    gdf=load_geojsondata()
    df['PYEONG']=df['BLDG_AREA']/3.3
    df['PYEONG']=df['PYEONG'].astype('int64')
    df['Pyeong_range']=df['PYEONG'].apply(Range)
    
    st.header('상세 검색')
    
    selected_house_type = st.selectbox(
        '용도를 선택하세요.',
        options=list(df['HOUSE_TYPE'].unique())
    )
    floor=st.number_input('층수를 입력하세요',step=1,min_value=-1,max_value=68)
    pyeong=st.number_input('평수를 입력하세요',step=1)
    buildyear=st.number_input('건축연도를 입력하세요',step=1)
    alpha=st.slider('오차범위를 선택하세요',0,5,1)
    
    filtered_df = df.loc[(df['HOUSE_TYPE']=='아파트')&
                         ((df['FLOOR']<=floor+alpha)&(df['FLOOR']>=floor-alpha))&
                         ((df['PYEONG']<=pyeong+alpha)&(df['PYEONG']>=pyeong-alpha))&
                         ((df['BUILD_YEAR']<=buildyear+alpha)&(df['BUILD_YEAR']>=buildyear-alpha))]
    
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
    
    

if __name__ == "__main__":
    main()