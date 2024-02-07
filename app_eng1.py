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

        # Create columns
        col5, col6, col7, col8 = st.columns(4)

        # Add content to columns
        with col5:
            st.markdown(f'<div style = "height: 220px; border: 1px solid white; padding: 10px; box-shadow: 2px,2px,5px rgba(0,0,0,0.1); "><h6 style ="text-align: center; color: gray;">Apartment</h6><h5 style="text-align: center; color: blue;">Highest Price</h5><h5 style = "text-align: center;">{values["아파트"]["max_amount"]:,.0f}10,000 Won<h5><h6>{values["아파트"]["max_location"]}<br>{values["아파트"]["max_building"]}</h6></div>', unsafe_allow_html=True)
        with col6:
            st.markdown(f'<div style = "height: 220px; border: 1px solid white; padding: 10px; box-shadow: 2px,2px,5px rgba(0,0,0,0.1); "><h6 style ="text-align: center; color: gray;">Officetel</h6><h5 style="text-align: center; color: blue;">Highest Price</h5><h5 style = "text-align: center;">{values["오피스텔"]["max_amount"]:,.0f}10,000 Won<h5><h6>{values["오피스텔"]["max_location"]}<br>{values["오피스텔"]["max_building"]}</h6></div>', unsafe_allow_html=True)
        with col7:
            st.markdown(f'<div style = "height: 220px; border: 1px solid white; padding: 10px; box-shadow: 2px,2px,5px rgba(0,0,0,0.1); "><h6 style ="text-align: center; color: gray;">Rowhouse multi-family</h6><h5 style="text-align: center; color: blue;">Highest Price</h5><h5 style = "text-align: center;">{values["연립다세대"]["max_amount"]:,.0f}10,000 Won<h5><h6>{values["연립다세대"]["max_location"]}<br>{values["연립다세대"]["max_building"]}</h6></div>', unsafe_allow_html=True)
        with col8:
            st.markdown(f'<div style = "height: 220px; border: 1px solid white; padding: 10px; box-shadow: 2px,2px,5px rgba(0,0,0,0.1); "><h6 style ="text-align: center; color: gray;">Single-family</h6><h5 style="text-align: center; color: blue;">Highest Price</h5><h5 style = "text-align: center;">{values["단독다가구"]["max_amount"]:,.0f}10,000 won<h5><h6>{values["단독다가구"]["max_location"]}<br>{values["단독다가구"]["max_building"]}</h6></div>', unsafe_allow_html=True)

        st.markdown("")

        # Create columns
        col9, col10, col11, col12 = st.columns(4)

        with col9:
            st.markdown(f'<div style = "height: 220px; border: 1px solid white; padding: 10px; box-shadow: 2px,2px,5px rgba(0,0,0,0.1); "><h6 style ="text-align: center; color: gray;">Apartment</h6><h5 style="text-align: center; color: red;">Lowest Price</h5><h5 style = "text-align: center;">{values["아파트"]["min_amount"]:,.0f}10,000 Won<h5><h6>{values["아파트"]["min_location"]}<br>{values["Apartment"]["min_building"]}</h6></div>', unsafe_allow_html=True)
        with col10:
            st.markdown(f'<div style = "height: 220px; border: 1px solid white; padding: 10px; box-shadow: 2px,2px,5px rgba(0,0,0,0.1); "><h6 style ="text-align: center; color: gray;">Officetel</h6><h5 style="text-align: center; color: red;">Lowest Price</h5><h5 style = "text-align: center;">{values["오피스텔"]["min_amount"]:,.0f}10,000 Won<h5><h6>{values["오피스텔"]["min_location"]}<br>{values["Officetel"]["min_building"]}</h6></div>', unsafe_allow_html=True)
        with col11:
            st.markdown(f'<div style = "height: 220px; border: 1px solid white; padding: 10px; box-shadow: 2px,2px,5px rgba(0,0,0,0.1); "><h6 style="text-align: center; color: gray;">Rowhouse Multi-family</h6><h5 style="text-align: center; color: red;">Lowest Price</h5><h5 style = "text-align: center;">{values["연립다세대"]["min_amount"]:,.0f}만원<h5><h6>{values["연립다세대"]["min_location"]}<br>{values["연립다세대"]["min_building"]}</h6></div>', unsafe_allow_html=True)
        with col12:
            st.markdown(f'<div style = "height: 220px; border: 1px solid white; padding: 10px; box-shadow: 2px,2px,5px rgba(0,0,0,0.1); "><h6 style="text-align: center; color: gray;">Single-family</h6><h5 style="text-align: center; color: red;">Lowest Price</h5><h5 style = "text-align: center;">{values["단독다가구"]["min_amount"]:,.0f}만원<h5><h6>{values["단독다가구"]["min_location"]}<br>{values["단독다가구"]["min_building"]}</h6></div>', unsafe_allow_html=True)
      

    # The page is displayed when the region is selected
    if selected_bjdong_nm != None:
        st.header('Real Estate Tracker: Seoul')
        tab1, tab2, tab3 = st.tabs(["Overview", "Detailed Search", "Comparison of Other Legal Districts"])
        with tab1:
            st.subheader('Transaction Amount')
            st.markdown(f'We compare the transaction amount of {selected_sgg_nm} {selected_bjdong_nm} with transactions across Seoul!')
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(label='Average (10,000 won)', value='{0:,}'.format(round(filtered_data.OBJ_AMT.mean(), 1)), delta='{0:,}'.format(round(filtered_data.OBJ_AMT.mean() - df.OBJ_AMT.mean(), 1)))
            with col2:
                st.metric(label='Maximum (10,000 won)', value='{0:,}'.format(round(filtered_data.OBJ_AMT.max(), 1)), delta=str('{0:,} '.format(round(filtered_data.OBJ_AMT.max() - df.OBJ_AMT.max(), 1))))
            with col3:
                st.metric(label='Minimum (10,000 won)', value='{0:,}'.format(round(filtered_data.OBJ_AMT.min(), 1)), delta=str('{0:,} '.format(round(filtered_data.OBJ_AMT.min() - df.OBJ_AMT.min(), 1))))

            st.divider()
            st.subheader('Monthly Transaction Count Trend')

            year = st.radio("Select a year.", ['2020', '2021', '2022', '2023'])
            filtered_data_year = filtered_data.loc[filtered_data['DEAL_YMD'].dt.year == int(year), :]
            st.line_chart(filtered_data_year['DEAL_YMD'].dt.month_name().value_counts())

            st.subheader('Building Use')
            st.bar_chart(filtered_data['HOUSE_TYPE'].value_counts())


        with tab2:
            options_df = ['OBJ_AMT_LV', 'HOUSE_TYPE', 'LAND_GBN_NM', 'DEAL_YMD', 'BUILD_YMD']
            options_dict = {'Product price range': 'OBJ_AMT_LV', 'Building type': 'HOUSE_TYPE', 'Land number code': 'LAND_GBN_NM', 'Transaction year': 'DEAL_YMD', 'Building year': 'BUILD_YEAR'}
            
            st.write(f'Check the information of interest among actual transactions in {selected_bjdong_nm}, {selected_sgg_nm}!')
            
            filtered_data_year['OBJ_AMT_LV'] = pd.cut(filtered_data_year['OBJ_AMT'], bins=[0, 10000, 50000, 100000, 150000, 200000, 3000000], labels=['Less than 100 million', '100 million to 500 million billion', '500 million to 1 billion', '1 billion to 2 billion', '2 billion to 2.5 billion', 'more than 2.5 billion'], include_lowest=True)
            filtered_data_year['DEAL_YMD'] = filtered_data_year['DEAL_YMD'].dt.year
            filtered_data_year['BUILD_YEAR'] = np.where(filtered_data_year['BUILD_YEAR'] == np.nan, 0, filtered_data_year['BUILD_YEAR'])
            filtered_data_year = filtered_data_year.astype({'BUILD_YEAR': 'str', 'DEAL_YMD': 'str'})
            filtered_data_year['BUILD_YEAR'] = filtered_data_year['BUILD_YEAR'].str[:4]
            options = st.selectbox('Select a keyword of interest.', options_dict.keys(), index=None)
            
            if options != None:
                st.divider()
                st.subheader('Keyword search results')
                st.caption('Click on each tab to check ascending (descending) order.')
                col = []
                key = options
                colname = options_dict[key]
                col.append(options_dict[key])
                table = pd.DataFrame(filtered_data_year.groupby(by=colname, observed=True))

                unique = []
                for i in table.iloc[:, 0]:
                    unique.append(i)
                selected_unique = st.radio('Select type to query', unique)
                st.write('Summary information by type')
                st.write(filtered_data_year[filtered_data_year[colname] == selected_unique].describe().T)

                st.write(f'View all data by type')
                if selected_unique == 'Single-family home':
                    st.caption('Note: For single-family homes, detailed information such as main number and sub-number is not provided.')
                st.write(filtered_data_year[filtered_data_year[colname] == selected_unique])
                st.divider()


    with tab3:
        st.write(f'Compare transactions in other neighborhoods with {selected_sgg_nm}!')
        option = st.selectbox('Search options', options=['Search by building information', 'Search by building price'])
        st.divider()

        if option == 'Search with building information':
            st.subheader(option)
            gdf = load_geojsondata()
            df['PYEONG'] = df['BLDG_AREA'] / 3.3
            df['PYEONG'] = df['PYEONG'].astype('int64')
            df['Pyeong_range'] = df['PYEONG'].apply(Range)

            selected_house_type = st.selectbox(
                'Choose your purpose.',
                options=list(df['HOUSE_TYPE'].unique())
            )
            floor = st.number_input('Enter the floor number', step=1, min_value=-1, max_value=68, value=1)
            pyeong = st.number_input('Enter the square footage', step=1, value=25)
            buildyear = st.number_input('Enter the year of construction', step=1, value=2010)
            alpha = st.slider('Select the error range', 0, 10, 2)

            filtered_df = df.loc[(df['HOUSE_TYPE'] == 'Apartment') &
                                ((df['FLOOR'] <= floor + alpha) & (df['FLOOR'] >= floor - alpha)) &
                                ((df['PYEONG'] <= pyeong + alpha) & (df['PYEONG'] >= pyeong - alpha)) &
                                ((df['BUILD_YEAR'] <= buildyear + alpha)) & (df['BUILD_YEAR'] >= buildyear - alpha)]

            avg_obj_amt = filtered_df.groupby('SGG_NM')['OBJ_AMT'].mean().reset_index()
            avg_obj_amt.columns = ['SGG_NM', 'Avg_Obj_Amt']

            # Merge geojson and dataframe
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
                                        labels={'Avg_Obj_Amt': 'Average transaction amount'},
                                        hover_data={'SGG_NM': True, 'Avg_Obj_Amt': True}
                                        )
            st.plotly_chart(fig)

        else:
            values = st.slider(
                'Set a price range for your building.',
                1000.0, 3000000.0, (10000.0, 300000.0))
            st.write('Price range:', values)

            # After setting the price range, other ward information within the same ward
            df = df.astype({'BUILD_YEAR': 'str'})
            df['BUILD_YEAR'] = df['BUILD_YEAR'].str.rstrip('.0')
            others = df.loc[(df.SGG_NM == selected_sgg_nm) & (df.BJDONG_NM != selected_bjdong_nm), :]
            others['DEAL_YMD'] = others['DEAL_YMD'].dt.date
            st.write(others.loc[(values[0] <= others.OBJ_AMT) & (others.OBJ_AMT <= values[1]), :])

            
if __name__ == "__main__":
    main()