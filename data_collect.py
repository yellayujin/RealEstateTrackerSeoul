import streamlit as st 
import pandas as pd
import geopandas as gpd

def load_data():
    df=pd.read_csv('https://raw.githubusercontent.com/ghkstod/TIL/main/data.txt',encoding='utf-8',sep='\t')
    df.drop(['Column1'],axis=1,inplace=True)
    df['DEAL_YMD'] = df['DEAL_YMD'].astype(str)
    df = df[~df['DEAL_YMD'].str.startswith('2019')]
    df = df[~df['DEAL_YMD'].str.startswith('2024')]
    df= df.drop_duplicates()
    df['Pyeong']=df['BLDG_AREA']/3.3
    df['Pyeong']=df['Pyeong'].astype('int64')
    df['Pyeong_range']=df['Pyeong'].apply(Range)

    return df

def Range(x):
    if x<10:
        return "10평 이하"
    elif x<20:
        return "10평대"
    elif x<30:
        return "20평대"
    elif x<40:
        return "30평대"
    elif x<50:
        return "40평대"
    elif x<60:
        return "50평대"
    elif x<70:
        return "60평대"
    elif x<80:
        return "70평대"
    elif x<90:
        return "80평대"
    elif x<100:
        return "90평대"
    else:
        return "100평대 이상"
    
def load_geojsondata():
    gdf=gpd.read_file('서울_자치구_경계_2017.geojson')
    return gdf




    