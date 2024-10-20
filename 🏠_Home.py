import streamlit as st

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

# Display the selected page
if page == "Home":
    home_page()
elif page == "Data":
    data_page()
elif page == "Predict":
    predict_page()
elif page == "History":
    history_page()
