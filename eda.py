import streamlit as st
import pandas as pd
from streamlit import StreamlitAPIException

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


def load_data(dataframe):
    for file in dataframe:
        df = pd.read_csv(file)
        return df


def show_data():
    data = st.file_uploader('Upload CSV Data File', type='csv',
                            accept_multiple_files=True)
    df = load_data(data)

    menu_eda = ['Descriptive', 'Plot']
    submenu = st.sidebar.selectbox('Submenu', menu_eda)

    if submenu == 'Descriptive':
        if df is not None:
            st.dataframe(df)
            with st.expander("Data Types"):
                dt = df.dtypes.astype(str)
                st.table(dt)

            data_menu = st.sidebar.selectbox('Data Columns',
                                             df.columns)

            with st.expander("Descriptive Summary"):
                for i in df.columns:
                    if data_menu == i:
                        try:
                            st.dataframe(df[i].describe())
                        except StreamlitAPIException:
                            st.error('Selected Column is Ordinal. Please Select Column with continuous Numerical Data')

            with st.expander("Class Distribution"):
                for i in df.columns:
                    if data_menu == i:
                        st.dataframe(df[i].value_counts())
    else:
        st.error('Second')
