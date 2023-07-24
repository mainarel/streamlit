import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def boxplot(table, column_name, groups = None):

    if groups == None:

        selected_column = table[column_name]

        fig, ax = plt.subplots()
        diagram = plt.boxplot(selected_column)
        ax.grid()
        ax.set_title(f'Boxplot "{column_name}"')
        ax.set_xlabel(f'"{column_name}"')

        return fig

    if groups is not None:

        array = table[[groups, column_name]]

        fig, ax = plt.subplots()
        diagram = sns.boxplot(x=groups, y=column_name, data = array)
        ax.grid()
        ax.set_title(f'Boxplots from "{column_name}" with steps "{groups}"')
        ax.set_xlabel(f'{groups}')
        ax.set_ylabel(f'{column_name}')
        
        return fig
    
def pie_diagram(table, column_name):

    column_name_counts = table[column_name].value_counts()

    fig, ax = plt.subplots()
    ax.set_title(f'Pie diagram {column_name}')
    diagram = plt.pie(column_name_counts, labels=column_name_counts.index, autopct=lambda x: f'{x:.2f}%', wedgeprops={'edgecolor': 'black', 'linewidth': 1})
    ax.legend(title=f'{column_name}', loc='center left', bbox_to_anchor=(1, 0.5))
        
    return fig