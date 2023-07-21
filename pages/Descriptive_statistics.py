import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import numpy as np
from data import get_data

st.set_page_config(
    page_title="Descriptive statistics",
    layout="centered")

st.image('2.jpg')

def descriptive_statistics(table, column_name):

    descriptive_statistics = table[column_name].describe()
    count_NAN = table[column_name].isnull().sum()

    SEM = table[column_name].describe().loc['std'] / np.sqrt(len(table) - count_NAN)

    descriptive_statistics_frame = descriptive_statistics.to_frame()
    descriptive_statistics_frame.loc['sem'] = [SEM] 

    return  descriptive_statistics_frame

def data_frequency(table, column_name):
    # pd.options.display.max_rows = 100

    selected_column = table[column_name]
    count_NAN = selected_column.isnull().sum()

    selected_column_freq = selected_column.value_counts(dropna = False).sort_index()
    selected_column_freq = selected_column_freq.to_frame()

    selected_column_freq['Percent'] = selected_column_freq[column_name] / selected_column_freq[column_name].sum() * 100
    selected_column_freq['Valid Percent'] = selected_column_freq[column_name] / (selected_column_freq[column_name].sum() - count_NAN) * 100


    selected_column_freq['Cumulative percent'] = selected_column_freq['Valid Percent'].cumsum()
    selected_column_freq.loc[np.nan,'Valid Percent'] = 0
    selected_column_freq.loc[np.nan,'Cumulative percent'] = np.nan


    selected_column_freq.loc['Total'] = selected_column_freq.sum()
    selected_column_freq.loc['Total','Cumulative percent'] = np.nan

    return selected_column_freq

def histogram_building(table, column_name, yerrors = None):

    selected_column = table[column_name]
    histogram = selected_column.value_counts(dropna = True).sort_index()

    fig, ax = plt.subplots()
    diag =  ax.bar(histogram.index.to_list(),  height=histogram.to_list(), align = 'center', yerr = yerrors)
    plt.figure(figsize=(15, 10))
    plt.rcParams.update({'font.size': 10})
    ax.set_title(f'Histogram {column_name}')
    ax.grid()
    ax.set_xlabel(f'{column_name}')
    ax.set_ylabel('Frequency')

    return fig



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