import streamlit as st
from basic.graphics import *
import pandas as pd


st.set_page_config(
    page_title="Diagrams builder",
    layout="wide")

st.markdown('## Diagrams builder')
uploaded_file  = st.file_uploader("Upload a .csv or .xlsx file with a maximum size of 200 mb", accept_multiple_files=False, type=['.csv', '.xlsx'])

if uploaded_file is not None:

    dataframe = pd.read_excel(uploaded_file)
    table = dataframe


    tab1_boxplot, tab2_pie = st.tabs(["Boxplot", "Pie"])

    with tab1_boxplot:

        options = st.multiselect('Select from 1 to 2 variables', list(table), max_selections = 2, help ='The first variable represents values on the y-axis, the second is responsible for groups on the x-axis')

        if len(options)==1:
            st.pyplot(boxplot(table,options[0]))
        
        if len(options)==2:
            st.pyplot(boxplot(table,options[0], options[1]))
    
    with tab2_pie:

        variable = st.selectbox( 'Select a variable ', list(table))
        st.write('You selected: ', variable)
        st.pyplot(pie_diagram(table,variable ))