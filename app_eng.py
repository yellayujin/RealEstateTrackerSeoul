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

Sure, here are comments explaining each function:

python
Copy code
def load_deals_by_month(df, year, month):
    # Function to retrieve transaction data corresponding to the specified year and month
    target_month = f'{year}-{month:02d}'  # Format year and month into YYYY-MM format
    deals = df[df['DEAL_YMD'].dt.to_period('M') == pd.Period(target_month, freq='M')]  # Filter dataframe by year and month
    deals['count'] = 1  # Add count column for each transaction
    deal_count = deals.shape[0]  # Count the number of deals
    return deals, deal_count  # Return filtered dataframe and deal count


def find_highest_increase_area(df, current_month, comparison_month):
    # Function to find the borough with the highest increase in transaction volume
    current_month_deals, current_month_deal_count = load_deals_by_month(df, *current_month)  # Load data for the current month
    comparison_month_deals, comparison_month_deal_count = load_deals_by_month(df, *comparison_month)  # Load data for the comparison month
    
    # Calculate transaction counts for current and comparison months by borough
    current_month_deal_counts = current_month_deals['SGG_NM'].value_counts()
    comparison_month_deal_counts = comparison_month_deals['SGG_NM'].value_counts()
    
    # Calculate percentage increase in transaction counts
    increase_rates = (current_month_deal_counts - comparison_month_deal_counts) / comparison_month_deal_counts * 100
    
    # Find the borough with the highest increase rate
    highest_increase_area = increase_rates.idxmax()
    highest_increase_rate = round(increase_rates.max(), 1)
    
    return highest_increase_area, highest_increase_rate  # Return borough with highest increase and its rate


def find_most_active_area(deals):
    # Function to find the borough with the highest transaction volume
    most_active_area = deals['SGG_NM'].value_counts().idxmax()  # Find borough with highest transaction count
    most_active_count = deals['SGG_NM'].value_counts().max()  # Get the count of transactions for the most active borough
    return most_active_area, most_active_count  # Return most active borough and its transaction count


def find_highest_avg_amt_area(df, year, month):
    # Function to find the borough with the highest average transaction amount
    target_month = f'{year}-{month:02d}'  # Format year and month into YYYY-MM format
    deals = df[df['DEAL_YMD'].dt.to_period('M') == pd.Period(target_month, freq='M')]  # Filter dataframe by year and month
    
    # Calculate average transaction amount by borough
    avg_amt_by_area = deals.groupby('SGG_NM')['OBJ_AMT'].mean()
    
    # Find the borough with the highest average transaction amount
    highest_avg_amt_area = avg_amt_by_area.idxmax()
    highest_avg_amt_value = avg_amt_by_area.max()
    
    return highest_avg_amt_area, highest_avg_amt_value  # Return borough with highest average amount and its value


def get_darker_color(color, factor=0.7):
    # Function to darken a given color by a specified factor
    r, g, b = [int(color[i:i + 2], 16) for i in (1, 3, 5)]  # Convert hex color to RGB
    r = max(0, int(r * factor))  # Darken red component
    g = max(0, int(g * factor))  # Darken green component
    b = max(0, int(b * factor))  # Darken blue component
    return f"#{r:02x}{g:02x}{b:02x}"  # Format RGB back to hex and return the darker color
These comments explain the purpose of each function and provide a brief description of what each part of the function does.

번역결과

물론입니다. 각 기능을 설명하는 설명은 다음과 같습니다.

python
Copy code
def load_deals_by_month(df, year, month):
    # Function to retrieve transaction data corresponding to the specified year and month
    target_month = f'{year}-{month:02d}'  # Format year and month into YYYY-MM format
    deals = df[df['DEAL_YMD'].dt.to_period('M') == pd.Period(target_month, freq='M')]  # Filter dataframe by year and month
    deals['count'] = 1  # Add count column for each transaction
    deal_count = deals.shape[0]  # Count the number of deals
    return deals, deal_count  # Return filtered dataframe and deal count


def find_highest_increase_area(df, current_month, comparison_month):
    # Function to find the borough with the highest increase in transaction volume
    current_month_deals, current_month_deal_count = load_deals_by_month(df, *current_month)  # Load data for the current month
    comparison_month_deals, comparison_month_deal_count = load_deals_by_month(df, *comparison_month)  # Load data for the comparison month
    
    # Calculate transaction counts for current and comparison months by borough
    current_month_deal_counts = current_month_deals['SGG_NM'].value_counts()
    comparison_month_deal_counts = comparison_month_deals['SGG_NM'].value_counts()
    
    # Calculate percentage increase in transaction counts
    increase_rates = (current_month_deal_counts - comparison_month_deal_counts) / comparison_month_deal_counts * 100
    
    # Find the borough with the highest increase rate
    highest_increase_area = increase_rates.idxmax()
    highest_increase_rate = round(increase_rates.max(), 1)
    
    return highest_increase_area, highest_increase_rate  # Return borough with highest increase and its rate


def find_most_active_area(deals):
    # Function to find the borough with the highest transaction volume
    most_active_area = deals['SGG_NM'].value_counts().idxmax()  # Find borough with highest transaction count
    most_active_count = deals['SGG_NM'].value_counts().max()  # Get the count of transactions for the most active borough
    return most_active_area, most_active_count  # Return most active borough and its transaction count


def find_highest_avg_amt_area(df, year, month):
    # Function to find the borough with the highest average transaction amount
    target_month = f'{year}-{month:02d}'  # Format year and month into YYYY-MM format
    deals = df[df['DEAL_YMD'].dt.to_period('M') == pd.Period(target_month, freq='M')]  # Filter dataframe by year and month
    
    # Calculate average transaction amount by borough
    avg_amt_by_area = deals.groupby('SGG_NM')['OBJ_AMT'].mean()
    
    # Find the borough with the highest average transaction amount
    highest_avg_amt_area = avg_amt_by_area.idxmax()
    highest_avg_amt_value = avg_amt_by_area.max()
    
    return highest_avg_amt_area, highest_avg_amt_value  # Return borough with highest average amount and its value


def get_darker_color(color, factor=0.7):
    # Function to darken a given color by a specified factor
    r, g, b = [int(color[i:i + 2], 16) for i in (1, 3, 5)]  # Convert hex color to RGB
    r = max(0, int(r * factor))  # Darken red component
    g = max(0, int(g * factor))  # Darken green component
    b = max(0, int(b * factor))  # Darken blue component
    return f"#{r:02x}{g:02x}{b:02x}" 


def plot_pie_chart(deals):
    colors = px.colors.sequential.Blues

    fig = px.pie(deals, 
                 names='SGG_NM', 
                 title='Percentage of transactions by Seoul borough',
                 color='SGG_NM',
                 color_discrete_sequence=colors,
                 labels={'SGG_NM': 'Borough'},
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
    fig = px.bar(deals, x = 'HOUSE_TYPE', title = 'Number of Real Estate Transactions by Type in May 2023', labels = {'HOUSE_TYPE': 'Property type', 'count': 'Transaction count'})
    fig.update_layout(xaxis_title = 'Property type', yaxis_title = 'Transaction count')
    st.plotly_chart(fig, use_container_width= True)


def main():
    
    df=load_data()
    df['DEAL_YMD'] = pd.to_datetime(df['DEAL_YMD'], format = '%Y%m%d') # Convert date type
    df['CNTL_YMD'] = pd.to_datetime(df['CNTL_YMD'], format = '%Y%m%d').dt.date
    df = df.astype({'ACC_YEAR': 'str', 'BONBEON': 'str', 'BUBEON': 'str'}) # The main number and sub-number are appended with .0 at the end (due to missing?), and the year of construction is I'll pass for a moment because of the calculations later (tab3, line 263).
    
    df['BONBEON'] = df['BONBEON'].str.rstrip('.0')
    df['BUBEON'] = df['BUBEON'].str.rstrip('.0')

    # sidebar
    with st.sidebar:
        st.header('🔎Local Search')  # Header for local search section
        st.subheader('We will analyze actual transaction data for the selected region!')  # Subheader explaining the purpose of the analysis
        
        # Select borough
        sgg_nm_sort = sorted(df['SGG_NM'].unique())  # Sort and get unique borough names
        selected_sgg_nm = st.selectbox(
            'Select a borough.',
            options=list(sgg_nm_sort), index=None
        )

        # Select a neighborhood within the selected borough
        selected_bjdong_nm = st.selectbox('Select Beopjeong-dong',
                                            options=sorted(df.loc[df['SGG_NM'] == selected_sgg_nm, :].BJDONG_NM.unique()), index=None)
        st.divider()
        
        # Home screen button
        
        # Select language
        st.subheader('Language')
        lang = st.radio('Select Your Language', ['English', 'Korean'], index=1)  # Radio button to choose language
        if lang == 'English':
            st.page_link('https://yellayujin-miniproject2-app-eng-aapmoa.streamlit.app/', label='Click here to explore in English')  # Link to explore in English

        st.divider()

    # Select the data you want to output
    filtered_data = df.loc[(df['SGG_NM'] == selected_sgg_nm) & (df['BJDONG_NM'] == selected_bjdong_nm)]

    if selected_bjdong_nm is None:
        # Styling for adding margins
        main_style = """
            padding: 10px;
            margin: 50px;
            """

        st.title('Real Estate Tracker: Seoul')  # Title for the Real Estate Tracker: Seoul section
        st.markdown('Check through the real estate tracker when you want to obtain information on the entire real estate transaction volume and statistics in Seoul and find out transaction trends by real estate type by region!')  # Description of the real estate tracker

        # Calculate trading volume for May 2023
        may_2023_deals, may_2023_deal_count = load_deals_by_month(df, 2023, 5)

        # Specify the month to compare with the current month
        current_month = {2023, 5}
        comparison_month = {2023, 4}

        # Find the borough with the highest transaction volume
        most_active_area, most_active_count = find_most_active_area(may_2023_deals)

        # Find the borough with the highest transaction volume growth
        highest_increase_area, highest_increase_rate = find_highest_increase_area(df, current_month, comparison_month)

        # Find the borough with the highest average transaction price
        highest_avg_amt_area, highest_avg_amt_value = find_highest_avg_amt_area(may_2023_deals, 2023, 5)

        # Create four columns
        col1, col2, col3, col4 = st.columns(4)

        # Add content to each cell
        st.caption('As of May 2023')  # Caption indicating the date
        with col1:
            # Display total transaction volume in Seoul
            st.markdown(f'<div style="border: 1px solid white; padding: 10px; box-shadow: 2px,2px,5px rgba(0,0,0,0.1); "><h6>Total transaction volume in Seoul</h6><br><br><h3 style="text-align: center;">{may_2023_deal_count}</h3><br></div>', unsafe_allow_html=True)
        with col2:
            # Display borough with the highest transaction volume increase
            st.markdown(f'<div style="border: 1px solid white; padding: 10px; box-shadow: 2px,2px,5px rgba(0,0,0,0.1);"><h6>Highest transaction volume Increased borough</h6><br><h3 style="text-align: center;">{highest_increase_area}<br><p style="text-align: right;">({highest_increase_rate}% increase )</div>', unsafe_allow_html=True)
        with col3:
            # Display borough with the highest transaction volume
            st.markdown(f'<div style="border: 1px solid white; padding: 10px; box-shadow: 2px,2px,5px rgba(0,0,0,0.1);"><h6>Highest transaction volume Many boroughs</h6><br><h3 style="text-align: center;">{most_active_area}<br><p style="text-align: right;">({most_active_count} cases increase) </div>', unsafe_allow_html=True)
        with col4:
            # Display borough with the highest average transaction price
            st.markdown(f'<div style="border: 1px solid white; padding: 10px; box-shadow: 2px,2px,5px rgba(0,0,0,0.1);">'
                        f'<h6>Borough with the highest average transaction price</h6>'
                        f'<br><h3 style="text-align: center; ">{highest_avg_amt_area}<br>'
                        f'<p style="text-align: right; ">({(highest_avg_amt_value*1000):,.0f} 10,000 won)</div>', unsafe_allow_html=True)

        # Draw a pie chart
        plot_pie_chart(may_2023_deals)

        # Initialize the maximum and minimum values for each building use
        values = {
            'apartment': {'max_amount': None, 'min_amount': None, 'max_location': None, 'min_location': None, 'max_building': None, 'min_building': None},
            'Officetel': {'max_amount': None, 'min_amount': None, 'max_location': None, 'min_location': None, 'max_building': None, 'min_building': None},
            'Multi-generational': {'max_amount': None, 'min_amount': None, 'max_location': None, 'min_location': None, 'max_building': None, 'min_building': None},
            'Single-family home': {'max_amount': None, 'min_amount': None, 'max_location': None, 'min_location': None, 'max_building': None, 'min_building': None}
        }

        for house_type in ['apartment', 'officetel', 'row multi-family', 'single-family multi-family']:
            # Filter data for the relevant building use
            filtered_data = df[df['HOUSE_TYPE'] == house_type]
            
            # Find the maximum and minimum values in the transaction amount ('OBJ_AMT') column
            max_amount = filtered_data['OBJ_AMT'].max()
            min_amount = filtered_data['OBJ_AMT'].min()
            
            # Find rows with maximum and minimum values
            max_row = filtered_data[filtered_data['OBJ_AMT'] == max_amount].iloc[0]
            min_row = filtered_data[filtered_data['OBJ_AMT'] == min_amount].iloc[0]

            # Save maximum and minimum values and location information
            values[house_type]['max_amount'] = max_amount
            values[house_type]['min_amount'] = min_amount
            values[house_type]['max_location'] = max_row['SGG_NM'] if not pd.isna(max_row['SGG_NM']) else ''
            values[house_type]['max_location'] += ' ' + max_row['BJDONG_NM'] if not pd.isna(max_row['BJDONG_NM']) else ''
            values[house_type]['max_building'] = max_row['BLDG_NM'] if not pd.isna(max_row['BLDG_NM']) else ''
            values[house_type]['min_location'] = min_row['SGG_NM'] if not pd.isna(min_row['SGG_NM']) else ''
            values[house_type]['min_location'] += ' ' + min_row['BJDONG_NM'] if not pd.isna(min_row['BJDONG_NM']) else ''
            values[house_type]['min_building'] = min_row['BLDG_NM'] if not pd.isna(min_row['BLDG_NM']) else ''

        # Subheader for displaying highest/minimum price information by building use in Seoul
        st.subheader("Highest/minimum price information by building use in Seoul")

