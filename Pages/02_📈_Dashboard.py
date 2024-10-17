import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Dashboard page content
def load_dashboard_page():
    st.title("Employee Attrition Dashboard")
    
    # Load dataset
    df = pd.read_csv('./Data/cleaned_data.csv')

    # Overall attrition count
    attrition_count = df['attrition'].value_counts()
    
    # Pie chart for attrition distribution
    st.subheader("Attrition Distribution")
    fig, ax = plt.subplots()
    ax.pie(attrition_count, labels=attrition_count.index, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures the pie chart is a circle.
    st.pyplot(fig)

    # Bar chart for attrition by department
    st.subheader("Attrition by Department")
    department_attrition = df.groupby('department')['attrition'].value_counts().unstack()
    department_attrition.plot(kind='bar', stacked=True)
    plt.title('Attrition by Department')
    plt.xlabel('Department')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    st.pyplot(plt)

    # Average salary by attrition status
    st.subheader("Average Salary by Attrition Status")
    avg_salary = df.groupby('attrition')['gross_salary'].mean().reset_index()
    sns.barplot(x='attrition', y='gross_salary', data=avg_salary)
    plt.title('Average Salary Based on Attrition Status')
    plt.ylabel('Average Gross Salary')
    st.pyplot(plt)

    # Additional analysis sections can be added here
    st.write("Explore the visualizations above to understand patterns related to employee attrition.")

# Load the dashboard page function
if __name__ == "__main__":
    load_dashboard_page()
