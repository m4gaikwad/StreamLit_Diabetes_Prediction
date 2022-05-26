import streamlit as st
import pandas as pd
from streamlit import StreamlitAPIException

import matplotlib.pyplot as plt
from matplotlib import colors
import seaborn as sns
import plotly.express as px


def load_data(dataframe):
    for file in dataframe:
        df = pd.read_csv(file)
        return df


def count_dataframe(dataframe, column):
    new_df = dataframe[column].value_counts().to_frame()
    new_df = new_df.reset_index()
    new_df.columns = [column, 'Count']
    return new_df


def show_summary(df, data_menu):
    for i in df.columns:
        if data_menu == i:
            try:
                st.dataframe(df[i].describe())
            except StreamlitAPIException:
                st.error('Selected Column is Categorical.'
                         'Please Select Column with '
                         'continuous Numerical Data')


def plot_distribution_bar(df, data_menu):
    for i in df.columns:
        try:
            if data_menu == i:
                try:
                    fig = plt.figure()
                    sns.countplot(df[i])
                    st.pyplot(fig)

                    new_df = count_dataframe(df, i)
                    st.dataframe(new_df)

                except StreamlitAPIException:
                    st.error('Select Another Column')
            else:
                continue
        except AttributeError:
            st.write('Upload Correct File')


def plot_count_pie(df, data_menu):
    for i in df.columns:
        try:
            if data_menu == i:
                try:
                    new_df = count_dataframe(df, i)
                    pi = px.pie(new_df, names=i, values='Count')
                    st.plotly_chart(pi, use_container_width=True)

                except StreamlitAPIException:
                    st.error('Select Another Column')
            else:
                continue
        except AttributeError:
            st.write('Upload Correct File')


def cust_hist(df, column):
    # legend = ['distribution']
    n_bins = [0, 10, 20, 30, 40, 50, 60, 70, 80]
    # Creating histogram
    fig, axs = plt.subplots(1, 1,
                            figsize=(10, 7),
                            tight_layout=True)

    # Remove axes splines
    for s in ['top', 'bottom', 'left', 'right']:
        axs.spines[s].set_visible(False)

    # Remove x, y ticks
    axs.xaxis.set_ticks_position('none')
    axs.yaxis.set_ticks_position('none')

    # Add padding between axes and labels
    axs.xaxis.set_tick_params(pad=5)
    axs.yaxis.set_tick_params(pad=10)

    # Add x, y gridlines
    axs.grid(b=True, color='grey',
             linestyle='-.', linewidth=0.5,
             alpha=0.6)

    # Add Text watermark
    fig.text(0.9, 0.15, 'Mayur Gaikwad',
             fontsize=12,
             color='red',
             ha='right',
             va='bottom',
             alpha=0.7)

    # Creating histogram
    N, bins, patches = axs.hist(df[column], bins=n_bins)

    # Setting color
    fracs = ((N ** (1 / 5)) / N.max())
    norm = colors.Normalize(fracs.min(), fracs.max())

    for thisfrac, thispatch in zip(fracs, patches):
        color = plt.cm.viridis(norm(thisfrac))
        thispatch.set_facecolor(color)

    # Adding extra features
    plt.xlabel(column)
    plt.ylabel('Count')
    # plt.legend(legend)
    plt.title(column + ' Distribution')

    # Show plot
    return plt


def plot_frequency_dist(df, data_menu):
    for i in df.columns:
        # try:
        if data_menu == i:
            try:
                fig = plt.figure()  # Comment this line for Customised Histogram
                sns.histplot(data=df, x=df[i], binwidth=10)  # Comment this line for Customised Histogram
                # fig = cust_hist(df, i) # Uncomment For Customised Histogram
                st.pyplot(fig)
            except StreamlitAPIException:
                st.error('Select Another Column')
        else:
            continue
    # except AttributeError:
    # st.write('Upload Correct File')


def boxplot(df, data_menu):
    for i in df.columns:
        if data_menu == i:
            try:
                fig = plt.figure()  # Uncomment to use Seaborn
                sns.boxplot(x=df[i])  # Uncomment to use Seaborn
                st.pyplot(fig)  # Uncomment to use Seaborn
                #bx = px.box(x=df[i], labels={'x': i})  # Uncomment to use Plotly
                #st.plotly_chart(bx, use_container_width=True)  # Uncomment to use Plotly

            except StreamlitAPIException:
                st.error('Select Another Column')
            except TypeError:
                st.error('Select Column with Numerical Data')
        else:
            continue


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
                show_summary(df, data_menu)

            with st.expander("Class Distribution"):
                for i in df.columns:
                    if data_menu == i:
                        st.dataframe(count_dataframe(df, i))

    elif submenu == 'Plot':
        st.subheader('Plot')

        if df is not None:
            col1, col2 = st.columns([1, 1])
            with col1:
                with st.expander('Distribution'):
                    plot_distribution_bar(df, data_menu)

            with col1:
                with st.expander('Box Plot'):
                    boxplot(df, data_menu)

            with col2:
                with st.expander('Distribution Pie Chart'):
                    plot_count_pie(df, data_menu)

                with st.expander('Frequency Distribution'):
                    plot_frequency_dist(df, data_menu)

            #with st.expander('Correlation'):
            #    corr_mat = df.corr()
            #    cor = plt.figure()
            #    sns.heatmap(corr_mat)
            #    st.pyplot(cor)

