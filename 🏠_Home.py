import streamlit as st
import pandas as pd
import joblib
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Set the page configuration
st.set_page_config(
    page_title="Home Page",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Home page content
def home_page():
    st.title("Employee Attrition Prediction App")
    st.subheader("Welcome to the Employee Attrition Prediction Application")
    st.write(
        """
        This application helps organizations predict employee attrition using 
        machine learning models. By analyzing past employee data, the app provides 
        insights into the likelihood of employees leaving the company.
        
        ## How to Use this App:
        - **Data Upload:** Upload the employee dataset in the required format.
        - **Data Analysis:** View summary statistics, visualize patterns, and understand key factors.
        - **Prediction:** Input new employee data to predict the likelihood of attrition.
        - **Results:** Review the predictions and take data-driven actions.
        
        ## About Employee Attrition
        Employee attrition refers to the gradual loss of employees over time. 
        High attrition rates can indicate dissatisfaction or issues within the 
        organization. Understanding the reasons behind attrition can help 
        organizations improve retention strategies.
        
        Use this app to identify at-risk employees and make informed decisions 
        to foster a more stable workforce.
        """
    )
    st.image("assets/HomePage.png", caption="Predicting Employee Attrition", use_column_width=True)
    st.write("Feel free to navigate to other sections using the sidebar.")

    # Links section
    st.subheader("Useful Links and Information")
    st.markdown("""
    - [GitHub Repository: Employee Attrition App](https://github.com/AndyMortey/Employee-Attrition-App)
    - [GitHub Repository: Employee Attrition Predictor](https://github.com/AndyMortey/Employee-Attrition-Predictor)
    """)

def data_page():
    st.title("Data Page")
    st.write("Upload and explore data here.")

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
# Sidebar content
with st.sidebar:
    st.header("Sidebar")

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv('./Data/cleaned_data.csv')

df = load_data()

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select a page:", ["KPI Dashboard", "EDA Dashboard"])

# KPI Dashboard
if page == "KPI Dashboard":
    st.title("KPI Dashboard")

    # Key Performance Indicators
    st.subheader("Key Performance Indicators")
    
    total_employees = df.shape[0]
    total_departments = df['department'].nunique()
    total_attrition_count = df['attrition'].value_counts().get('Yes', 0)
    attrition_rate = df['attrition'].value_counts(normalize=True)['Yes'] * 100
    average_age = df['age'].mean()
    average_length_of_service = df['length_of_service'].mean()

    # Display KPIs
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Employees", total_employees)
    col2.metric("Total Departments", total_departments)
    col3.metric("Total Attrition Count", total_attrition_count)

    col4, col5 = st.columns(2)
    col4.metric("Attrition Rate (%)", round(attrition_rate, 2))
    col5.metric("Average Age", round(average_age, 2))

    st.metric("Average Length of Service (Years)", round(average_length_of_service, 2))

    st.write("Use this dashboard to monitor the key metrics related to employee attrition.")

# EDA Dashboard
elif page == "EDA Dashboard":
    st.title("Exploratory Data Analysis Dashboard")

    # Attrition Distribution
    st.subheader("Attrition Distribution")
    attrition_count = df['attrition'].value_counts()
    fig, ax = plt.subplots()
    ax.pie(attrition_count, labels=attrition_count.index, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)

    # Attrition by Department
    st.subheader("Attrition by Department")
    department_attrition = df.groupby('department')['attrition'].value_counts().unstack()
    department_attrition.plot(kind='bar', stacked=True)
    plt.title('Attrition by Department')
    plt.xlabel('Department')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    st.pyplot(plt)

    # Average Salary by Attrition Status
    st.subheader("Average Salary by Attrition Status")
    avg_salary = df.groupby('attrition')['gross_salary'].mean().reset_index()
    sns.barplot(x='attrition', y='gross_salary', data=avg_salary)
    plt.title('Average Salary Based on Attrition Status')
    plt.ylabel('Average Gross Salary')
    st.pyplot(plt)

    st.write("Explore the visualizations above to understand patterns related to employee attrition.")

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
def predict_page():
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

# History Page
def history_page():
    st.title("Prediction History")

# Function to load history data
@st.cache_data(persist=True)
def load_history():
    csv_path = "Data/history.csv"  # Adjust the path accordingly
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    else:
        return pd.DataFrame()  # Return an empty DataFrame if file doesn't exist

def display_history_of_all_predictions():
    st.title("Prediction History📄")

    # Button to clear cache
    if st.button("Clear Cache"):
        st.cache_data.clear()

    # Load history data
    history = load_history()

    # Check if the history DataFrame is not empty
    if not history.empty:
        st.write("Here are the past predictions:")
        st.dataframe(history)
        
        # Download option for the history data
        st.subheader("Download Data")
        st.download_button(
            label="Download history as CSV",
            data=history.to_csv(index=False).encode('utf-8'),
            file_name='prediction_history.csv',
            mime='text/csv'
        )
    else:
        st.write("No history of predictions yet.")
# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Data", "Predict", "History"])

# Display the selected page
if page == "Home":
    home_page()
elif page == "Data":
    data_page()
elif page == "Predict":
    predict_page()
elif page == "History":
    history_page()
