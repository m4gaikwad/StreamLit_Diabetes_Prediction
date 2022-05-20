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

    if df is not None:
        data_menu = st.sidebar.selectbox('Data Columns',
                                        df.columns)

    if submenu == 'Descriptive':
        st.subheader('Descriptive Summary')
        if df is not None:
            st.dataframe(df)
            with st.expander("Data Types"):
                dt = df.dtypes.astype(str)
                st.table(dt)

            with st.expander("Descriptive Summary"):
                for i in df.columns:
                    if data_menu == i:
                        try:
                            st.dataframe(df[i].describe())
                        except StreamlitAPIException:
                            st.error('Selected Column is Categorical.'
                                     'Please Select Column with '
                                     'continuous Numerical Data')

            with st.expander("Class Distribution"):
                for i in df.columns:
                    if data_menu == i:
                        st.dataframe(df[i].value_counts())

    elif submenu == 'Plot':
        st.subheader('Plot')

        if df is not None:
            col1, col2 = st.columns([1, 1])
            with col1:
                with st.expander('Distribution'):
                    for i in df.columns:
                        try:

                            if data_menu == i:
                                try:
                                    fig = plt.figure()
                                    sns.countplot(df[i])
                                    st.pyplot(fig)

                                    new_df = df[i].value_counts().to_frame()
                                    new_df = new_df.reset_index()
                                    new_df.columns = [i, 'Count']
                                    st.dataframe(new_df)

                                except StreamlitAPIException:
                                    st.error('Select Another Column')
                            else:
                                continue
                        except AttributeError:
                            st.write('Upload Correct File')

            with col2:
                with st.expander('Distribution Pie Chart'):
                    for i in df.columns:
                        try:
                            if data_menu == i:
                                try:
                                    new_df = df[i].value_counts().to_frame()
                                    new_df = new_df.reset_index()
                                    new_df.columns = [i, 'Count']
                                    #st.dataframe(new_df)

                                    pi = px.pie(new_df, names=i, values='Count')
                                    st.plotly_chart(pi, use_container_width=True)

                                except StreamlitAPIException:
                                    st.error('Select Another Column')
                            else:
                                continue
                        except AttributeError:
                            st.write('Upload Correct File')
