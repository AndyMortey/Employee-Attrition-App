import streamlit as st
import pandas as pd
import joblib  # or import pickle
import numpy as np

# Set page configuration
st.set_page_config(
    page_title="Predict Attrition",
    page_icon="🔍",
    layout="wide"
)

# Load the trained model
@st.cache_resource
def load_model():
    model = joblib.load('./Model/best_gb_model_and_threshold.pkl')  # Update path as necessary
    return model

model = load_model()

# Preprocess input function (modify according to your preprocessing steps)
def preprocess_input(input_data):
    # Convert input data to DataFrame
    df = pd.DataFrame([input_data])
    
    # Apply the same preprocessing as done during training
    # Example: Encoding categorical variables, scaling numerical features, etc.
    
    # Example of encoding categorical features (modify as necessary)
    df['department'] = df['department'].astype('category').cat.codes
    df['education_field'] = df['education_field'].astype('category').cat.codes
    df['marital_status'] = df['marital_status'].astype('category').cat.codes
    df['attrition'] = df['attrition'].astype('category').cat.codes

    # Return the processed DataFrame
    return df

# Prediction page
st.title("Employee Attrition Prediction")

# Input fields
st.subheader("Enter Employee Details")

# Input form for employee data
department = st.selectbox("Department", options=['Personal Finance', 'Tech Department', 'Brokerage', 'Management',
 'Client Services', 'Legal and Admin', 'Customer Service', 'Portfolio',
 'Human Resource', 'Marketing Department', 'Human Resources',
 'Strategic Initiatives', 'Relationship Mgt'])
education_field = st.selectbox("Education Field", options=['Finance', 'Computer Science', 'Business Mgt', 'Business Admin', 'Law'
 'Social Science', 'Human Resources', 'Marketing'])
marital_status = st.selectbox("Marital Status", options=["Single", "Married"])
age = st.number_input("Age", min_value=18, max_value=100, value=30)
length_of_service = st.number_input("Length of Service (Years)", min_value=0, max_value=40, value=1)
gross_salary = st.number_input("Gross Salary", min_value=1000, max_value=200000, value=50000)
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
        "work_life_balance": work_life_balance,
        "job_satisfaction": job_satisfaction,
        "attrition": "Unknown"  # or any placeholder value if attrition is to be determined
    }
    
    # Preprocess the input data
    processed_data = preprocess_input(input_data)

    # Make prediction
    prediction = model.predict(processed_data)
    
    # Display prediction
    if prediction[0] == 1:  # Assuming 1 indicates attrition
        st.success("The employee is likely to leave the company.")
    else:
        st.success("The employee is likely to stay with the company.")

# Main function to run the app
if __name__ == "__main__":
    st.write("Use this page to predict employee attrition based on input data.")
