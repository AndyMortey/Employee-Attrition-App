import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from Utils.info import column_1, column_2

# Page configuration
st.set_page_config(
    page_title='Home',
    layout='wide',
    page_icon='🏠'
)

# Load the configuration from config.yaml
with open('./config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Initialize the authenticator
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# Authenticate users
login_response = authenticator.login(location='sidebar')

if login_response is not None:
    name, authentication_status, username = login_response

    # Display the home page if authentication is successful
    if st.session_state['authentication_status']:
        authenticator.logout(location='sidebar')
        st.title('Attrition Predictor')

        col1, col2 = st.columns(2)
        with col1:
            column_1
        with col2:
            column_2

    # Display an error if authentication fails
    elif st.session_state['authentication_status'] is False:
        st.error('Wrong username/password')

    # Display a login prompt if no authentication is provided
    elif st.session_state['authentication_status'] is None:
        st.info('Login to get access to the app')
        st.code("""
        Test Account
        Username: attritionapp
        Password: 123456
        """)
else:
    st.error("Login failed. Please try again.")
