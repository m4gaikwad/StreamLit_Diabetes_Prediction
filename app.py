import pandas as pd
import streamlit as st
import streamlit.components.v1 as stc
import eda
import ml

html_temp = """
		<div style="background-color:#3872fb;padding:10px;border-radius:10px">
		<h1 style="color:white;text-align:center;">Early Stage DM Risk Data App </h1>
		<h4 style="color:white;text-align:center;">Diabetes </h4>
		</div>
		"""


def main():
    stc.html(html_temp)
    menu = ['Home', 'EDA', 'ML']
    choice = st.sidebar.selectbox('Menu', menu)

    if choice == 'Home':
        st.subheader('Home')

    elif choice == 'EDA':
        st.subheader('EDA')
        eda.show_data()

    else:
        st.subheader('ML Prediction')
        ml.calculate()


if __name__ == '__main__':
    main()
