import streamlit as st
import pandas as pd
import streamlit_authenticator as stauth

# Initialize 'page' in session state
if 'page' not in st.session_state:
    st.session_state['page'] = 'Data'

# Home page content placeholder
def main():
    st.title("Home Page")
    st.write("Welcome to the Employee Attrition Prediction App!")

# Dashboard page placeholder
def load_dashboard():
    st.title("Dashboard")
    st.write("This is the Dashboard page.")

# Prediction page placeholder
def load_predict_page():
    st.title("Prediction Page")
    st.write("This is the Prediction page.")

# History page placeholder
def load_history_page():
    st.title("History")
    st.write("This is the History page.")

# Data page content
def load_data_page():
    st.title("Data Upload and Overview")
    st.subheader("Dataset Overview")

    # Load dataset
    df = pd.read_csv('./Data/cleaned_data.csv')

    # Full dataset section
    st.markdown("<h2 style='font-size:24px;'>Full Dataset</h2>", unsafe_allow_html=True)

    # Dataset filtering options
    selection = st.selectbox(
        "Select columns to display:",
        options=["All columns", "Numerical columns", "Categorical columns"]
    )

    # Define numerical and categorical columns
    numerical_columns = ['age', 'education_level', 'environment_satisfaction', 
                         'job_satisfaction', 'gross_salary', 'work_life_balance', 
                         'length_of_service']
    categorical_columns = ['department', 'education_field', 'marital_status', 'attrition']

    # Filter the DataFrame based on user selection
    if selection == "Numerical columns":
        df_filtered = df[numerical_columns]
    elif selection == "Categorical columns":
        df_filtered = df[categorical_columns]
    else:
        df_filtered = df

    # Sidebar Navigation Menu
    st.sidebar.title("Navigation")
    st.session_state['page'] = st.sidebar.selectbox("Select Page", ["Home", "Data", "Dashboard", "Predict", "History"])

    # Display the filtered DataFrame
    st.subheader("Filtered Data Preview")
    st.dataframe(df_filtered.head())

    # Display basic statistics for numerical columns only
    if selection in ["All columns", "Numerical columns"]:
        st.subheader("Data Summary")
        st.write("Below are some basic statistics of the numerical data:")
        st.write(df_filtered.describe())

    # Show column data types
    st.subheader("Column Data Types")
    st.write("The following are the data types for each column:")
    st.write(df.dtypes)

    # Display shape of the dataset
    st.subheader("Dataset Information")
    st.write(f"Number of rows: {df.shape[0]}")
    st.write(f"Number of columns: {df.shape[1]}")

# Page Routing Logic
if __name__ == "__main__":
    if st.session_state['page'] == "Home":
        main()
    elif st.session_state['page'] == "Data":
        load_data_page()
    elif st.session_state['page'] == "Dashboard":
        load_dashboard()
    elif st.session_state['page'] == "Predict":
        load_predict_page()
    elif st.session_state['page'] == "History":
        load_history_page()
