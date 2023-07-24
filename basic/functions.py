import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


def data_types(table):

    return table.dtypes.to_frame()

def data_shape(table):
        
    count_lines, count_columns = table.shape 

    return count_lines, count_columns


def pairplot(table, grouping = None, kind = 'scatter', diag_kind='auto'):

    plt.figure(figsize=(10,8), dpi= 150)
    diagram = sns.pairplot(table, kind=kind, hue = grouping, diag_kind  = diag_kind)
    return diagram

def correlation_diagram(table):
    
    plt.figure(figsize=(25,20), dpi= 160)
    plt.title('Correlation diagram', fontsize=22)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)

    diagram = sns.heatmap(table.corr(), xticklabels=table.corr().columns, yticklabels=table.corr().columns, cmap='RdYlGn', center=0, annot=True)

    return diagram.figure, table.corr()

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
