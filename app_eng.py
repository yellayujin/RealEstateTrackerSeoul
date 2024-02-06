# -*- coding:utf-8 -*-

import streamlit as st 
import pandas as pd
from data_collect import load_data
from data_collect import Range  
from data_collect import load_geojsondata   
import plotly.express as px 
import plotly.graph_objects as go 
from datetime import datetime
import requests
from io import StringIO

def load_deals_by_month(df, year, month):
    # Load transaction data for the specified year and month
    target_month = f'{year}-{month:02d}'
    deals = df[df['DEAL_YMD'].dt.to_period('M') == pd.Period(target_month, freq='M')]
    deals['count'] = 1  # Add a count column
    deal_count = deals.shape[0]
    return deals, deal_count

def find_highest_increase_area(df, current_month, comparison_month):
    # Load transaction data for the reference month
    current_month_deals, current_month_deal_count = load_deals_by_month(df, *current_month)

    # Load transaction data for the comparison month
    comparison_month_deals, comparison_month_deal_count = load_deals_by_month(df, *comparison_month)

    # Calculate the transaction volume for the reference and comparison months
    current_month_deal_counts = current_month_deals['SGG_NM'].value_counts()
    comparison_month_deal_counts = comparison_month_deals['SGG_NM'].value_counts()

    # Calculate the increase rate in transaction volume
    increase_rates = (current_month_deal_counts - comparison_month_deal_counts) / comparison_month_deal_counts * 100

    # Find the district with the highest increase rate
    highest_increase_area = increase_rates.idxmax()
    highest_increase_rate = round(increase_rates.max(), 1)

    return highest_increase_area, highest_increase_rate

def find_most_active_area(deals):
    # Find the district with the highest transaction volume
    most_active_area = deals['SGG_NM'].value_counts().idxmax()
    most_active_count = deals['SGG_NM'].value_counts().max()
    return most_active_area, most_active_count

def find_highest_avg_amt_area(df, year, month):
    # Load transaction data for the specified year and month
    target_month = f'{year}-{month:02d}'
    deals = df[df['DEAL_YMD'].dt.to_period('M') == pd.Period(target_month, freq='M')]

    # Calculate the average OBJ_AMT by district
    avg_amt_by_area = deals.groupby('SGG_NM')['OBJ_AMT'].mean()

    # Find the district with the highest average value
    highest_avg_amt_area = avg_amt_by_area.idxmax()
    highest_avg_amt_value = avg_amt_by_area.max()

    return highest_avg_amt_area, highest_avg_amt_value

def get_darker_color(color, factor=0.7):
    """
    Function to get a darker shade of a given color.
    """
    r, g, b = [int(color[i:i+2], 16) for i in (1, 3, 5)]
    r = max(0, int(r * factor))
    g = max(0, int(g * factor))
    b = max(0, int(b * factor))
    return f"#{r:02x}{g:02x}{b:02x}"

def plot_pie_chart(deals):
    colors = px.colors.sequential.Blues

    fig = px.pie(deals, 
                 names='SGG_NM', 
                 title='Transaction Ratio by Autonomous District in Seoul, May 2023',
                 color='SGG_NM',
                 color_discrete_sequence=colors,
                 labels={'SGG_NM': 'District Name'},
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
    fig = px.bar(deals, x='HOUSE_TYPE', title='Real Estate Transactions by Type in Seoul, May 2023', labels={'HOUSE_TYPE': 'Property Type', 'count': 'Number of Transactions'})
    fig.update_layout(xaxis_title='Property Type', yaxis_title='Number of Transactions')
    st.plotly_chart(fig, use_container_width=True)

def main():
    
    df = load_data()

    # Sidebar
    # Search data by code?
    with st.sidebar:
        st.header('Filter')
        st.subheader('We will analyze actual transaction data for the selected region!')
        # Choose autonomous district
        selected_sgg_nm = st.selectbox('District Name', options=df['SGG_NM'].unique(), index=None, placeholder='Select a district.')

        # Choose a dong (Condition: Show only neighborhoods within the selected district)
        selected_bjdong_nm = st.selectbox('Legal Dong Name',
                                          options=df.loc[df['SGG_NM'] == selected_sgg_nm, :].BJDONG_NM.unique())
        st.divider()
        
        # Home screen button

        # Select language
        st.subheader('Language')
        lang = st.radio('Select Your Language', ['English', 'Korean'], index=0)
        if lang == 'Korean':
            st.page_link('https://yellayujin-miniproject2-app-dlixks.streamlit.app/', label='Click here to explore in Korean') 
                
        st.divider()


    # Select the data you want to output
    filtered_data = df.loc[(df['SGG_NM'] == selected_sgg_nm) & (df['BJDONG_NM'] == selected_bjdong_nm)]


    if selected_bjdong_nm == None:
        # Styling for adding margins
        main_style = """
            padding: 10px;
            margin: 50px;
            """

        st.title('dashboard name')
        st.markdown('Introductory text')


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


        # Create four spaces
        col1, col2, col3, col4 = st.columns(4)
    
        # Add content to each cell
        st.caption('As of May 2023')
        with col1:
            st.markdown(f'<div style="border: 1px solid white; padding: 10px; box-shadow: 2px,2px,5px rgba(0,0,0,0.1); "><h6>Total transaction volume in Seoul</h6><br><br><h3 style="text-align: center;">{may_2023_deal_count}</h3><br></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div style="border: 1px solid white; padding: 10px; box-shadow: 2px,2px,5px rgba(0,0,0,0.1);"><h6>Highest transaction volume <br>Increased borough</h6><br><h3 style="text-align: center;">{highest_increase_area}<br><p style="text-align: right;">({highest_increase_rate}% increase )</div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div style="border: 1px solid white; padding: 10px; box-shadow: 2px,2px,5px rgba(0,0,0,0.1);"><h6>Highest transaction volume<br>Many boroughs</h6><br><h3 style="text-align: center;">{most_active_area}<br><p style="text-align: right;">({most_active_count} cases increase) </div>', unsafe_allow_html=True)
        with col4:
            st.markdown(f'<div style="border: 1px solid white; padding: 10px; box-shadow: 2px,2px,5px rgba(0,0,0,0.1);">'
                    f'<h6>Borough with the highest average transaction price</h6>'
                    f'<br><h3 style="text-align: center; ">{highest_avg_amt_area}<br>'
                    f'<p style="text-align: right; ">({(highest_avg_amt_value*1000): ,.0f} 10,000 won)</div>', unsafe_allow_html=True)

        # Draw a pie chart
        plot_pie_chart(may_2023_deals)


    # The page is displayed when the region is selected
    if selected_bjdong_nm != None:
        tab1, tab2, tab3 = st.tabs(["At a glance", "Keyword detailed search", "Comparison of other legal districts"])
        with tab1:
            st.subheader('Transaction Amount')
            st.markdown('We show the transaction amount in the selected area by comparing it with the transactions in the entire city of Seoul!')
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(label='Mean (10,000 won)', value=round(filtered_data.OBJ_AMT.mean(), 1), delta=round(filtered_data.OBJ_AMT.mean() - df.OBJ_AMT.mean(), 1 ))
            with col2:
                st.metric(label='Maximum (10,000 won)', value=round(filtered_data.OBJ_AMT.max(), 1), delta=str(round(filtered_data.OBJ_AMT.max() - df.OBJ_AMT.max() , 1)))
            with col3:
                st.metric(label='Minimum (10,000 won)', value=round(filtered_data.OBJ_AMT.min(), 1), delta=str(round(filtered_data.OBJ_AMT.min() - df.OBJ_AMT.min() , 1)))

            st.divider()
            st.subheader('Number of transactions')
            # Comparison of transaction number trends in 2020, 21, 22, and 23??

            # Transaction date in date format
            # filtered_data['DEAL_YMD_dt'] = pd.to_datetime(filtered_data['DEAL_YMD'], format='ISO8601')

            # Trading volume by year -> It would be good to combine each year into one graph.
            year = st.radio("Select a year.", ['2020', '2021', '2022', '2023'])
            filtered_data_year = filtered_data.loc[filtered_data['DEAL_YMD'].dt.year == int(year), :]
            st.line_chart(filtered_data_year['DEAL_YMD'].dt.month_name().value_counts())


            # Building use
            st.subheader('Building Use')
            st.bar_chart(filtered_data['HOUSE_TYPE'].value_counts())

        with tab2:
            st.write(f'{selected_sgg_nm} Check the information of interest among {selected_bjdong_nm}\'s actual transactions!')
            options = st.multiselect(
                'Select a keyword of interest.',
                filtered_data.columns)
            if len(options) != 0:
                st.divider()
                st.write('Keyword search results')
                st.caption('Click on each tab to check ascending (descending) order.')
                st.write(filtered_data[options])
            

        with tab3:
            # st.header('Detailed search')
            st.write(f'{selected_sgg_nm} Check out my other consent transactions!')
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
                floor = st.number_input('Enter the floor number', step=1, min_value=-1, max_value=68)
                pyeong = st.number_input('Enter the square footage', step=1)
                buildyear = st.number_input('Enter the year of construction', step=1)
                alpha = st.slider('Select the error range', 0, 10, 1)
                
                filtered_df = df.loc[(df['HOUSE_TYPE'] == 'Apartment') &
                                     ((df['FLOOR'] <= floor + alpha) & (df['FLOOR'] >= floor - alpha)) &
                                     ((df['PYEONG'] <= pyeong + alpha) & (df['PYEONG'] >= pyeong - alpha)) &
                                     ((df['BUILD_YEAR'] <= buildyear + alpha) & (df['BUILD_YEAR'] >= buildyear - alpha))]
                
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
                                           zoom=10,
                                           center={"lat": 37.5650172, "lon": 126.9782914},
                                           opacity=0.5,
                                           labels={'Avg_Obj_Amt': 'Average transaction amount'},
                                           hover_data={'SGG_NM': True, 'Avg_Obj_Amt': True}
                                           )
                st.plotly_chart(fig)
            
            # After setting the price range, show other ward information within the same ward
            else:
                values = st.slider(
                    'Select a range of values',
                    1000.0, 100000.0, (1000.0, 4000.0))
                st.write('Price range:', values)

                others = df.loc[(df.SGG_NM == selected_sgg_nm) & (df.BJDONG_NM != selected_bjdong_nm), :]
                st.write(others.loc[(values[0] <= others.OBJ_AMT) & (others.OBJ_AMT <= values[1]), :])

if __name__ == "__main__":
    main()


