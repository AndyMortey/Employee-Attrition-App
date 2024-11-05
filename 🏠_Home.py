import streamlit as st
import streamlit_authenticator as stauth

# Set the page configuration
st.set_page_config(
    page_title="Home Page",
    page_icon="🏠",
    layout="wide"
)

# Initialize 'page' in session state
if 'page' not in st.session_state:
    st.session_state['page'] = 'Home'

# Home page content
def main():
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

    # Sidebar Navigation Menu
    st.sidebar.title("Navigation")
    st.session_state['page'] = st.sidebar.selectbox("Select Page", ["Home", "Data", "Dashboard", "Predict", "History"])

    # Links section
    st.subheader("Useful Links and Information")
    st.markdown("""
    - [GitHub Repository: Employee Attrition App](https://github.com/AndyMortey/Employee-Attrition-App)
    - [GitHub Repository: Employee Attrition Predictor](https://github.com/AndyMortey/Employee-Attrition-Predictor)
    """)

    st.image("assets/HomePage.png", caption="Predicting Employee Attrition", use_column_width=True)
    st.write("Feel free to navigate to other sections using the sidebar.")

# Page Routing Logic
if __name__ == "__main__":
    if st.session_state['page'] == "Home":
        main()
    elif st.session_state['page'] == "Data":
        # Define and call your data page function
        pass
    elif st.session_state['page'] == "Dashboard":
        # Define and call your dashboard function
        pass
    elif st.session_state['page'] == "Predict":
        # Define and call your prediction page function
        pass
    elif st.session_state['page'] == "History":
        # Define and call your history page function
        pass
