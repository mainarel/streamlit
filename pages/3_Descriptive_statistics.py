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
    
   
    

    variables = st.multiselect('Select variables to display descriptive statistics', list(table.select_dtypes(include='number')), default=None)
    st.write('WARNING: Only numeric columns available! ')
    if len(variables) > 0:
        st.write(descriptive_statistics(table, variables))
        st.write('You selected: ', variables)
    else:
        st.write('Descriptive statistics of all numeric variables:')
        st.write(descriptive_statistics(table))
    
    
    variable_for_histogram = st.selectbox('Select variables to display histogram', list(table))
    st.pyplot(histogram_building(table,variable_for_histogram))

  
  
    # st.write(data_frequency(table,variable))
