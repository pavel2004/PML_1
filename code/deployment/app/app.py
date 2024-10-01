# File: code/deployment/app/app.py
import streamlit as st
import requests
import pandas as pd

# Define the FastAPI endpoint URL
API_URL = "http://api:8000/predict"

# Streamlit app title
st.title('Titanic Survival Prediction App')

# User input form
st.header('Enter Passenger Details:')
Pclass = st.selectbox('Passenger Class (1 = 1st, 2 = 2nd, 3 = 3rd)', [1, 2, 3])
Sex = st.selectbox('Sex', ['male', 'female'])
SibSp = st.number_input('Number of Siblings/Spouses Aboard', min_value=0, max_value=10, value=0)
Parch = st.number_input('Number of Parents/Children Aboard', min_value=0, max_value=10, value=0)

# Submit button
if st.button('Predict Survival'):
    # Prepare data to send to the API
    passenger_data = {
        "Pclass": Pclass,
        "Sex": Sex,
        "SibSp": SibSp,
        "Parch": Parch
    }
    
    # Make a request to the FastAPI API
    response = requests.post(API_URL, json=passenger_data)
    
    # Handle the response
    if response.status_code == 200:
        result = response.json()
        survived = result['Survived']
        if survived == 1:
            st.success("The passenger survived.")
        else:
            st.error("The passenger did not survive.")
    else:
        st.error("Error in prediction request.")
