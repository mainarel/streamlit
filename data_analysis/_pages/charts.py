import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def show_charts(df):
    # Подзаголовок
    st.subheader("Графики")

    # Пример графика
    fig, ax = plt.subplots()
    df["Age"].plot(kind="bar", ax=ax)
    ax.set_title("Age Distribution")
    ax.set_xlabel("Person")
    ax.set_ylabel("Age")
    st.pyplot(fig)
