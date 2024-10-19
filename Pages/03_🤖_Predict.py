import streamlit as st
import pandas as pd
import joblib
import numpy as np
import os

# Set page configuration
st.set_page_config(
    page_title="Predict Attrition",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar content
with st.sidebar:
    st.header("Sidebar")

# Load the trained model and encoder
@st.cache_resource
def load_model_and_encoder():
    model, threshold = joblib.load('./Model/best_gb_model_and_threshold.pkl')
    encoder = joblib.load('./Model/encoder copy.joblib')
    return model, threshold, encoder

model, threshold, encoder = load_model_and_encoder()

# Preprocess input function (modify according to your preprocessing steps)
def preprocess_input(input_data):
    # Convert input data to DataFrame
    df = pd.DataFrame([input_data])

    # Replace unseen labels with 'Other'
    if df['department'][0] not in encoder.classes_:
        df['department'] = 'Other'
    if df['education_field'][0] not in encoder.classes_:
        df['education_field'] = 'Other'
    if df['marital_status'][0] not in encoder.classes_:
        df['marital_status'] = 'Other'

    # Transform the columns
    df['department'] = encoder.transform(df[['department']])
    df['education_field'] = encoder.transform(df[['education_field']])
    df['marital_status'] = encoder.transform(df[['marital_status']])

    # Return the processed DataFrame
    return df

# Function to save prediction history
def save_prediction(input_data, prediction):
    # Create a DataFrame from input data and prediction
    df = pd.DataFrame([input_data])
    df['prediction'] = 'Likely to Leave' if prediction == 1 else 'Likely to Stay'

    # Path to save the history file
    history_file = 'Data/history.csv'
    
    # Check if history file exists, append or create a new one
    if os.path.exists(history_file):
        df.to_csv(history_file, mode='a', header=False, index=False)
    else:
        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(history_file), exist_ok=True)
        df.to_csv(history_file, index=False)

# Prediction page
st.title("Employee Attrition Prediction")

# Input fields
st.subheader("Enter Employee Details")

# Input form for employee data
department = st.selectbox("Department", options=['Personal Finance', 'Tech Department', 'Brokerage', 'Management',
 'Client Services', 'Legal and Admin', 'Customer Service', 'Portfolio',
 'Human Resource', 'Marketing Department', 'Human Resources',
 'Strategic Initiatives', 'Relationship Mgt'])
education_field = st.selectbox("Education Field", options=['Finance', 'Computer Science', 'Business Mgt', 'Business Admin', 'Law',
 'Social Science', 'Human Resources', 'Marketing'])
marital_status = st.selectbox("Marital Status", options=["Single", "Married"])
age = st.number_input("Age", min_value=18, max_value=100, value=30)
length_of_service = st.number_input("Length of Service (Years)", min_value=0, max_value=40, value=1)
gross_salary = st.number_input("Gross Salary", min_value=1000, max_value=200000, value=50000)
education_level = st.selectbox("Education Level", options=[1, 2])
environment_satisfaction = st.selectbox("Environment Satisfaction", options=[1, 2, 3, 4])
work_life_balance = st.selectbox("Work Life Balance", options=[1, 2, 3, 4])
job_satisfaction = st.selectbox("Job Satisfaction", options=[1, 2, 3, 4])

# Button to predict
if st.button("Predict Attrition"):
    input_data = {
        "department": department,
        "education_field": education_field,
        "marital_status": marital_status,
        "age": age,
        "length_of_service": length_of_service,
        "gross_salary": gross_salary,
        "education_level": education_level,
        "environment_satisfaction": environment_satisfaction,
        "work_life_balance": work_life_balance,
        "job_satisfaction": job_satisfaction
    }
    
    # Preprocess the input data
    processed_data = preprocess_input(input_data)
    prediction = model.predict(processed_data)[0]

   # Save the prediction to history
    save_prediction(input_data, prediction)
    
    # Display prediction
    if prediction == 1:
        st.success("The employee is likely to leave the company.")
    else:
        st.success("The employee is likely to stay with the company.")

