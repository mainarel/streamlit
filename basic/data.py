import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd


@st.cache_data
def get_data():
    return pd.read_excel('test.xlsx')