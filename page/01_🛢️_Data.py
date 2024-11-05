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

# Main function to run the app
if __name__ == "__main__":
    st.write("Navigate between the KPI and EDA dashboards using the sidebar.")

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
    if st.session_state['page'] == "Data":
        load_data_page()
    elif st.session_state['page'] == "Dashboard":
        load_dashboard()
    elif st.session_state['page'] == "Predict":
        load_predict_page()
    elif st.session_state['page'] == "History":
        load_history_page()
