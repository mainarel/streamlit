import streamlit as st
from basic.functions import *
import pandas as pd

st.set_page_config(
    page_title="Descriptive statistics",
    layout="wide")

st.image('2.jpg')

uploaded_file  = st.file_uploader("Upload a .csv or .xlsx file with a maximum size of 200 mb", accept_multiple_files=False, type=['.csv', '.xlsx'])

if uploaded_file is not None:

    dataframe = pd.read_excel(uploaded_file)
    table = dataframe

    st.markdown('## Descriptive statistics')
    variable = st.selectbox( 'Select a variable ', list(table))

    st.write('You selected: ', variable)
    st.write(descriptive_statistics(table, variable))
    st.write(data_frequency(table,variable))
    st.pyplot(histogram_building(table,variable))