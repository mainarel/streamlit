import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu


# Импортируем функции из модулей, но не сами модули
def load_data():
    df = pd.read_csv("data/my_database.csv")
    return df


# Загрузка данных
df = load_data()

# Заголовок приложения
st.title("Аналитика данных")

# Создание бокового меню с помощью option_menu
with st.sidebar:
    selected = option_menu(
        menu_title="Навигация",
        options=["Главная", "Обзор данных", "Кросс-таблица", "Графики"],
        icons=["🏠", "📊", "", "📈"],
        default_index=0,
    )

# Обработка выбранной вкладки
if selected == "Главная":
    st.write("Это главная страница")

elif selected == "Обзор данных":

    from _pages.data_overview import *

    tab1_all, tab2_columns = st.tabs(["All", "Columns"])

    with tab1_all:
        show_page(df)
        data_shape(df)
        displayTypes(df)
        countsNulls(df)
        show_categorical_columns_and_unique_values(df)

        isDuplicateRows(df)

    with tab2_columns:
        with st.expander("Описательная статистика", expanded=True):
            descriptiveStatistics(
                df,
                numeric_columns=df.select_dtypes(include=["number"]).columns.tolist(),
                non_numeric_columns=df.select_dtypes(
                    exclude=["number"]
                ).columns.tolist(),
            )

        with st.expander("Статистика по столбцам", expanded=True):
            generateSummary(df)

elif selected == "Кросс-таблица":

    from _pages.data_overview import generate_cross_table

    st.title("Кросс-таблица данных")

    # Мультиселект для выбора столбцов по вертикали
    vertical_columns = st.multiselect(
        "Выберите столбцы для вертикальных категорий", df.columns.tolist()
    )

    # Мультиселект для выбора столбцов по горизонтали
    horizontal_columns = st.multiselect(
        "Выберите столбцы для горизонтальных категорий", df.columns.tolist()
    )

    # Мультиселект для выбора типов агрегации
    aggregation_types = st.multiselect(
        "Выберите типы агрегации", ["sample", "percent", "mean"]
    )

    # Выбор столбца для агрегации
    values_column = st.selectbox(
        "Выберите столбец для агрегации данных", ["sample", "percent", "mean"]
    )

    if vertical_columns and horizontal_columns and aggregation_types and values_column:
        # Генерируем кросс-таблицу
        cross_table_data = generate_cross_table(
            df, vertical_columns, horizontal_columns, values_column, aggregation_types
        )

        if cross_table_data is not None:
            # Отображаем результаты
            st.dataframe(cross_table_data)
    else:
        st.warning("Выберите все необходимые параметры для создания кросс-таблицы")

elif selected == "Графики":

    from _pages.charts import *

    show_charts(df)
