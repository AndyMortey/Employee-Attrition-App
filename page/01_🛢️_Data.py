import streamlit as st
import pandas as pd
import streamlit_authenticator as stauth

# Load dataset
@st.cache_data
def load_data():
    try:
        return pd.read_csv('./Data/cleaned_data.csv')
    except FileNotFoundError:
        st.error("The dataset file could not be found. Please ensure that './Data/cleaned_data.csv' exists.")
        return pd.DataFrame()  # Return an empty DataFrame if loading fails

# Display dataset overview
def display_data_overview(df):
    st.title("Data Upload and Overview")
    st.subheader("Dataset Overview")

    if df.empty:
        st.warning("No data to display.")
        return

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

# Sidebar Navigation
def sidebar_navigation():
    st.sidebar.title("Navigation")
    if 'page' not in st.session_state:
        st.session_state['page'] = "Home"
    st.session_state['page'] = st.sidebar.selectbox("Select Page", ["Home", "Data", "Dashboard", "Predict", "History"])

# Main function
def load_data_page():
    df = load_data()
    sidebar_navigation()
    display_data_overview(df)

# Load the data page function
if __name__ == "__main__":
    load_data_page()
