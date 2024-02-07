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


    st.write("서울시 건물용도별 최고가/최소가 정보")

    # 칸 생성
    col5, col6, col7, col8 = st.columns(4)

    # 칸에 내용 추가
    with col5:
        st.markdown(f'<div style = "border: 1px solid white; padding: 10px; box-shadow: 2px,2px,5px rgba(0,0,0,0.1); "><h6 style="text-align: center; color: gray;">아파트</h6><h5 style="text-align: center; color: blue;">최고가</h5><h5 style = "text-align: center;">{values["아파트"]["max_amount"]:,.0f}만원<h5><h6>{values["아파트"]["max_location"]}<br>{values["아파트"]["max_building"]}</h6></div>', unsafe_allow_html=True)
    with col6:
        st.markdown(f'<div style = "border: 1px solid white; padding: 10px; box-shadow: 2px,2px,5px rgba(0,0,0,0.1); "><h6 style="text-align: center; color: gray;">아파트</h6><h5 style="text-align: center; color: blue;">최고가</h5><h5 style = "text-align: center;">{values["오피스텔"]["max_amount"]:,.0f}만원<h5><h6>{values["오피스텔"]["max_location"]}<br>{values["오피스텔"]["max_building"]}</h6></div>', unsafe_allow_html=True)  
    with col7:
        st.markdown(f'<div style = "border: 1px solid white; padding: 10px; box-shadow: 2px,2px,5px rgba(0,0,0,0.1); "><h6 style="text-align: center; color: gray;">아파트</h6><h5 style="text-align: center; color: blue;">최고가</h5><h5 style = "text-align: center;">{values["연립다세대"]["max_amount"]:,.0f}만원<h5><h6>{values["연립다세대"]["max_location"]}<br>{values["연립다세대"]["max_building"]}</h6></div>', unsafe_allow_html=True)
    with col8:
        st.markdown(f'<div style = "border: 1px solid white; padding: 10px; box-shadow: 2px,2px,5px rgba(0,0,0,0.1); "><h6 style="text-align: center; color: gray;">아파트</h6><h5 style="text-align: center; color: blue;">최고가</h5><h5 style = "text-align: center;">{values["단독다가구"]["max_amount"]:,.0f}만원<h5><h6>{values["단독다가구"]["max_location"]}<br>{values["단독다가구"]["max_building"]}</h6></div>', unsafe_allow_html=True)
    

    st.markdown("")


    # 칸 생성
    col9, col10, col11, col12 = st.columns(4)

    with col9:
        st.markdown(f'<div style = "border: 1px solid white; padding: 10px; box-shadow: 2px,2px,5px rgba(0,0,0,0.1); "><h6 style="text-align: center; color: gray;">아파트</h6><h5 style="text-align: center; color: red;">최저가</h5><h5 style = "text-align: center;">{values["아파트"]["min_amount"]:,.0f}만원<h5><h6>{values["아파트"]["min_location"]}<br>{values["아파트"]["min_building"]}</h6></div>', unsafe_allow_html=True)
    with col10:
        st.markdown(f'<div style = "border: 1px solid white; padding: 10px; box-shadow: 2px,2px,5px rgba(0,0,0,0.1); "><h6 style="text-align: center; color: gray;">오피스텔</h6><h5 style="text-align: center; color: red;">최저가</h5><h5 style = "text-align: center;">{values["오피스텔"]["min_amount"]:,.0f}만원<h5><h6>{values["오피스텔"]["min_location"]}<br>{values["오피스텔"]["min_building"]}</h6></div>', unsafe_allow_html=True)
    with col11:
        st.markdown(f'<div style = "border: 1px solid white; padding: 10px; box-shadow: 2px,2px,5px rgba(0,0,0,0.1); "><h6 style="text-align: center; color: gray;">연립다세대</h6><h5 style="text-align: center; color: red;">최저가</h5><h5 style = "text-align: center;">{values["연립다세대"]["min_amount"]:,.0f}만원<h5><h6>{values["연립다세대"]["min_location"]}<br>{values["연립다세대"]["min_building"]}</h6></div>', unsafe_allow_html=True)
    with col12:
        st.markdown(f'<div style = "border: 1px solid white; padding: 10px; box-shadow: 2px,2px,5px rgba(0,0,0,0.1); "><h6 style="text-align: center; color: gray;">단독다가구</h6><h5 style="text-align: center; color: red;">최저가</h5><h5 style = "text-align: center;">{values["단독다가구"]["min_amount"]:,.0f}만원<h5><h6>{values["단독다가구"]["min_location"]}<br>{values["단독다가구"]["min_building"]}</h6></div>', unsafe_allow_html=True)
      
