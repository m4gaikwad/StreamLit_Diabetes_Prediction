import streamlit as st

import joblib
import os
attrib_info = """
#### Attribute Information:
    - Age 1.20-65
    - Sex 1. Male, 2.Female
    - Polyuria 1.Yes, 2.No.
    - Polydipsia 1.Yes, 2.No.
    - sudden weight loss 1.Yes, 2.No.
    - weakness 1.Yes, 2.No.
    - Polyphagia 1.Yes, 2.No.
    - Genital thrush 1.Yes, 2.No.
    - visual blurring 1.Yes, 2.No.
    - Itching 1.Yes, 2.No.
    - Irritability 1.Yes, 2.No.
    - delayed healing 1.Yes, 2.No.
    - partial paresis 1.Yes, 2.No.
    - muscle stiness 1.Yes, 2.No.
    - Alopecia 1.Yes, 2.No.
    - Obesity 1.Yes, 2.No.
    - Class 1.Positive, 2.Negative.

"""
label_dict = {'No':0,'Yes':1}
gender_map = {'Female':0,'Male':1}
target_label_map = {'Negative':0,'Positive':1}

"""
'age','gender','polyuria','polydipsia','sudden_weight_loss',
 'weakness','polyphagia','genital_thrush','visual_blurring',
 'itching','irritability','delayed_healing','partial_paresis',
 'muscle_stiffness','alopecia','obesity','class']
"""

def get_fvalue(val):
    feature_dict = label_dict
    for key,value in feature_dict.items():
        if val == key:
            return value

def get_value(val,my_dict):
    for key,value in my_dict.items():
        if val == key:
            return value

@st.cache
def load_model(model):
    loaded_model = joblib.load(open(os.path.join(model),'rb'))
    return loaded_model

def calculate():
    submenu = ['Logistic Regression', 'Decision Tree']
    model = st.sidebar.selectbox('Model',submenu)

    with st.expander('Attribute Info'):
        st.markdown(attrib_info)

    #Layout
    col1,col2 = st.columns(2)

    with col1:
        age = st.number_input('Age',min_value=10,max_value=100)
        gender = st.radio('Gender',['Female','Male'])
        polyuria = st.radio('Polyuria', ['Yes', 'No'])
        polydipsia = st.radio('Polydipsia', ['Yes', 'No'])
        sudden_weight_loss= st.radio('Sudden Weight Loss', ['Yes', 'No'])
        weakness = st.selectbox('Weakness', ['Yes', 'No'])
        polyphagia = st.selectbox('Polyphagia', ['Yes', 'No'])
        genital_thrush = st.select_slider('Genital Thrush', ['Yes', 'No'])


    with col2:
        visual_blurring = st.selectbox('Visual Blurring', ['Yes', 'No'])
        itching = st.radio('Itching', ['Yes', 'No'])
        irritability = st.radio('Irritability', ['Yes', 'No'])
        delayed_healing = st.radio('Delayed Healing', ['Yes', 'No'])
        partial_paresis = st.radio('Partial Paresis', ['Yes', 'No'])
        muscle_stiffness = st.radio('Muscle Stiffness', ['Yes', 'No'])
        alopecia = st.select_slider('Alopecia', ['Yes', 'No'])
        obesity = st.selectbox('Obesity', ['Yes', 'No'])

    submit =st.button('Submit')
    if submit:
        with st.expander('Selected Options Are:'):
            result = {'age': age,
                      'gender': gender,
                      'polyuria': polyuria,
                      'polydipsia': polydipsia,
                      'sudden_weight_loss':sudden_weight_loss,
                      'weakness':weakness,
                      'polyphagia':polyphagia,
                      'genital_thrush':genital_thrush,
                      'visual_blurring':visual_blurring,
                      'itching':itching,
                      'irritability':irritability,
                      'delayed_healing':delayed_healing,
                      'partial_paresis':partial_paresis,
                      'muscle_stiffness':muscle_stiffness,
                      'alopecia':alopecia,
                      'obesity':obesity
                      }
            st.write(result)

            encoded_result = []
            for i in result.values():
                if type(i) == int:
                    encoded_result.append(i)
                elif i in ['Female','Male']:
                    res = get_value(i,gender_map)
                else:
                    encoded_result.append(get_fvalue(i))

            st.write(encoded_result)