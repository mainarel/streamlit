import streamlit as st
import pandas as pd
from io import StringIO
from basic.functions import *


st.set_page_config(
    page_title="Data Overview",
    page_icon="📑",
    layout="wide",
)

st.image('1.jpg')

st.markdown(
    """
    ### Database mapping, variable types and table size
    \n  
    """
)

uploaded_file  = st.file_uploader("Upload a .csv or .xlsx file with a maximum size of 200 mb", accept_multiple_files=False, type=['.csv', '.xlsx'])

if uploaded_file is not None:
    # To read file as bytes:
    # bytes_data = uploaded_file.getvalue()
    # st.write(bytes_data)

    # # To convert to a string based IO:
    # stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    # st.write(stringio)

    # # To read file as string:
    # string_data = stringio.read()
    # st.write(string_data)

    # Can be used wherever a "file-like" object is accepted:

    dataframe = pd.read_excel(uploaded_file)

    if st.checkbox('Show dataframe'):
        st.markdown('## Uploaded dataset')
        st.write(dataframe)

    table = dataframe

    st.markdown('## Types of data')
    st.write(data_types(table))

    st.markdown('## Table size')
    st.write('In this table ', data_shape(table)[0], ' lines and ', data_shape(table)[1],' columns')

    if st.checkbox('Pairwise relationships'):

        st.markdown('## Pairwise relationships')

        option_kind = st.selectbox('Kind of plot to make', ['scatter', 'kde', 'hist', 'reg'])
        st.write('You selected "kind":', option_kind)

        option_diag_kind = st.selectbox('Kind of plot for the diagonal subplots. If ‘auto’, choose based on whether or not "hue" is used', ['auto', 'hist', 'kde', 'None'])
        st.write('You selected "diag_kind":', option_diag_kind)

        st.pyplot(pairplot(table, kind = option_kind, diag_kind=option_diag_kind ))

    if st.checkbox('Correlation diagram'):

        st.markdown('## Correlation diagram')

        st.write(correlation_diagram(table)[1])
        st.pyplot(correlation_diagram(table)[0])
        
        





    