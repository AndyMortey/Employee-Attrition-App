import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit_authenticator as stauth

# Set page configuration
st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)

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
