import matplotlib.pyplot as plt
import streamlit as st



st.set_page_config(
    page_title="Welcome page",
    page_icon="👋",
    layout="centered")

#logo
st.image('cats_logo.jpg')

# Main Description
st.markdown("## 👋 Welcome to Stat_Main, your best tool to compare and explore mathematical statistics and data science!")
st.markdown("Developed by __mainarel__: https://github.com/mainarel")
st.markdown("The app is still under development and is used for the purpose of mastering data analysis tools in python. Please reach me in the github repo if you have any comments or suggestions.")

# Description of the features. 
st.markdown(
    """
    ### Select on the left panel what you want to explore:

    - With 📑 Data overview, you will get the main characteristics of the database
    
    \n  
    
    """
)



