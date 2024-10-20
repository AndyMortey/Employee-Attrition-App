import streamlit as st
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth

# Set the page configuration
st.set_page_config(
    page_title="Home Page",
    page_icon="🏠",
    layout="wide"
)

# Load configuration for authentication
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Create authenticator object
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

# Authentication
try:
    name, authentication_status, username = authenticator.login(location="sidebar")
except Exception as e:
    st.error(f"Authentication error: {e}")

# Home page content
def home_page():
    if st.session_state.get("authentication_status"):
        authenticator.logout("Logout", "sidebar")
        st.title(f"Welcome, {name}!")
        st.write("You're logged in. Navigate using the sidebar to access different sections.")
        
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
    else:
        st.title("Employee Attrition Prediction App")
        st.warning("Please log in to access the app.")

if __name__ == "__main__":
    home_page()
