import streamlit as st
import pandas as pd
import requests

BASE_URL = 'http://localhost:48884/route-sample/'

@st.cache_data
def get_title():
    title_url = BASE_URL + 'title'
    res = requests.get(title_url)
    if res.status_code == 200:
        return res.json()

st.title(get_title())

@st.cache_data
def get_levels():
    name_list = []
    elevation_list = []
    level_url = BASE_URL + 'levels'
    res = requests.get(level_url)
    if res.status_code == 200:
        for l in res.json():
                name_list.append(l['name'])
                elevation_list.append(l['Elevation'])
        level_tuple = list(zip(name_list, elevation_list))

    table_data = pd.DataFrame(
            level_tuple,
            columns = ['レベル名','エレベーション']
    )
    return table_data
st.dataframe(get_levels())

option = st.selectbox(
     '分類',
     ('ファミリ', 'ファミリタイプ')
)
furniture_url = BASE_URL + 'furnitures'
res = requests.get(furniture_url)
if res.status_code == 200:
    if option == 'ファミリ':
        furniture_dict = res.json()['family']
    elif option == 'ファミリタイプ':
         furniture_dict = res.json()['family_type']
furniture_data = pd.DataFrame(
    furniture_dict.values(),
    index=furniture_dict.keys()     
)
st.bar_chart(furniture_data)
