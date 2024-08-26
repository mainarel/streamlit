import streamlit as st
import pandas as pd
import base64
from io import BytesIO
import numpy as np


def data_shape(df):
    st.subheader("Размерность датафрейма")
    st.write(f"В базе {df.shape[0]} строк и {df.shape[1]} столбцов")


def isDuplicateRows(df):
    st.subheader("Дубликаты")
    st.write("Количество дубликатов: ", df.duplicated().sum())
    # if st.button("Удалить дубликаты"):
    #     df.drop_duplicates(inplace=True)
    #     st.success("Дубликаты удалены")


def displayTypes(df):
    st.subheader("Типы данных в столбцах")
    st.dataframe(df.dtypes.to_frame().rename(columns={0: "type"}))


def countsNulls(df):
    st.subheader("Количество пустых значений в столбцах")
    st.dataframe(df.isnull().sum().to_frame().rename(columns={0: "counts_null"}))


def show_categorical_columns_and_unique_values(df):
    # Получаем список категориальных столбцов
    categorical_columns = df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()
    st.subheader("Просмотр уникальных значений")
    # Выбираем столбец из выпадающего списка
    selected_column = st.selectbox(
        "Выберите категориальный столбец", options=categorical_columns, index=None
    )

    # Выводим уникальные значения выбранного столбца
    if selected_column:
        unique_values = df[selected_column].unique()
        st.write(f"Уникальные значения столбца '{selected_column}':")
        st.write(unique_values)


def descriptiveStatistics(df, numeric_columns, non_numeric_columns):

    show_numeric = st.checkbox("Для числовых столбцов")
    show_non_numeric = st.checkbox("Для нечисловых столбцов")

    if show_numeric:
        selected_numeric_columns = st.multiselect(
            "Выберите числовые столбцы", numeric_columns, default=numeric_columns
        )
        if selected_numeric_columns:
            st.write(df[selected_numeric_columns].describe())

    if show_non_numeric:
        selected_non_numeric_columns = st.multiselect(
            "Выберите нечисловые столбцы",
            non_numeric_columns,
            default=non_numeric_columns,
        )
        if selected_non_numeric_columns:
            st.write(df[selected_non_numeric_columns].describe())


def generateSummary(df):
    selected_columns = st.multiselect(
        "Выберите столбцы для анализа", df.columns.tolist()
    )
    if selected_columns is None:
        selected_columns = df.columns.tolist()

    summary_data = []

    # Перебираем выбранные столбцы датафрейма
    for column in selected_columns:
        # Получаем уникальные значения и их частоты
        value_counts = df[column].value_counts(dropna=False)
        total_count = len(df)

        cumulative_percent = 0  # Начальное значение накопительного процента

        # Создаем строки для каждого уникального значения
        for value, count in value_counts.items():
            percent = (count / total_count) * 100
            cumulative_percent += percent  # Увеличиваем накопительный процент

            # Ограничиваем накопительный процент максимум 100%
            if cumulative_percent > 100:
                cumulative_percent = 100

            summary_data.append(
                {
                    "var_name": column,
                    "unique_value": value,
                    "count": count,
                    "percent": percent,
                    "cumulative_percent": cumulative_percent,
                }
            )

    # Создаем новый датафрейм из собранных данных
    summary_df = pd.DataFrame(summary_data)

    st.dataframe(summary_df)


def get_agg_func(df, agg_type, values):
    if agg_type == "sample":
        return len
    elif agg_type == "percent":
        return lambda x: len(x) / len(df) * 100 if len(x) > 0 else np.nan
    elif agg_type == "mean":
        return "mean"
    else:
        raise ValueError(f"Unsupported aggregation type: {agg_type}")


def generate_cross_table(df, rows, cols, values, aggregation_types):
    # Проверяем, что выбранные столбцы существуют в датафрейме
    if not set(rows).issubset(df.columns) or not set(cols).issubset(df.columns):
        st.warning("Выбранные столбцы не существуют в датафрейме")
        return None

    # Создаем кросс-таблицу с выбранными столбцами по вертикали и горизонтали
    cross_table = pd.crosstab(
        index=df[rows],
        columns=df[cols],
        values=df[values],
        aggfunc={
            agg_type: get_agg_func(df, agg_type, values)
            for agg_type in aggregation_types
        },
    )
    return cross_table


def create_download_button(df, file_format, file_name):
    buffer = BytesIO()
    # Конвертируем датафрейм в нужный формат
    if file_format == "csv":

        file_content = df.to_csv(index=False)
        b64 = base64.b64encode(file_content.encode()).decode()
        href = f"data:{file_format};base64,{b64}"

    elif file_format == "xlsx":

        with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
            df.to_excel(writer, sheet_name="Sheet1", index=False)

        # Получаем содержимое объекта BytesIO в виде байтов
        excel_data = buffer.getvalue()

        # Кодируем данные в base64
        b64 = base64.b64encode(excel_data).decode()

        href = f"data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}"
    else:
        raise ValueError("Unsupported file format. Supported formats: 'csv', 'excel'.")

    # Кодируем данные в base64

    st.download_button(
        label=f"Скачать {file_name}, {file_format}",
        data=href,
        file_name=f"{file_name}.{file_format}",
    )


def show_page(df):
    # Подзаголовок
    st.subheader("Обзор данных")

    # Фильтры по столбцам
    columns_to_filter = st.multiselect("Выберите столбцы для фильтрации", df.columns)

    # Создаем пустой датафрейм, который будем фильтровать
    filtered_df = df.copy()

    # Добавляем фильтры для выбранных столбцов
    for col in columns_to_filter:
        # Выбираем тип виджета в зависимости от типа данных в столбце
        if pd.api.types.is_numeric_dtype(df[col]):
            # В числовых столбцах используем ползунок для выбора диапазона
            min_value = df[col].min()
            max_value = df[col].max()
            filter_min, filter_max = st.slider(
                f"Выберите диапазон для столбца '{col}'",
                min_value,
                max_value,
                (min_value, max_value),
            )
            filtered_df = filtered_df[
                (filtered_df[col] >= filter_min) & (filtered_df[col] <= filter_max)
            ]
        else:
            # В остальных столбцах используем multiselect для выбора нескольких значений
            filter_values = st.multiselect(
                f"Выберите значения для столбца '{col}'", df[col].unique().tolist()
            )
            if filter_values:
                filtered_df = filtered_df[filtered_df[col].isin(filter_values)]

    # Отображение отфильтрованного DataFrame
    st.dataframe(filtered_df)

    # Кнопка для скачивания отфильтрованного датафрейма в CSV

    create_download_button(filtered_df, "csv", "filtered_data")
    create_download_button(filtered_df, "xlsx", "filtered_data")
