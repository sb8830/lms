import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import os

# Load configuration from YAML file
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Create an authentication object
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

# Render the login widget
name, authentication_status, username = authenticator.login('Login', 'main')

# Handle authentication status
if authentication_status:
    authenticator.logout('Logout', 'main')
    st.sidebar.write(f'Welcome *{name}*')

    # Retrieve user role
    user_role = config['credentials']['usernames'][username]['role']

    # Define available modes based on role
    if user_role == 'admin':
        mode = st.sidebar.selectbox('Select Mode', ['Admin Control', 'Backend LMS', 'Customer Site'])
    elif user_role == 'backend':
        mode = 'Backend LMS'
    elif user_role == 'customer':
        mode = 'Customer Site'
    else:
        st.error('Invalid role assigned.')
        st.stop()

    # Navigate to the selected mode
    if mode == 'Admin Control':
        st.experimental_set_query_params(page='admin_control')
    elif mode == 'Backend LMS':
        st.experimental_set_query_params(page='backend_lms')
    elif mode == 'Customer Site':
        st.experimental_set_query_params(page='customer_site')

    # Load the corresponding page
    page = st.experimental_get_query_params().get('page', [''])[0]
    if page == 'admin_control':
        import pages.admin_control as admin_control
        admin_control.run()
    elif page == 'backend_lms':
        import pages.backend_lms as backend_lms
        backend_lms.run()
    elif page == 'customer_site':
        import pages.customer_site as customer_site
        customer_site.run()
    else:
        st.write("Please select a mode from the sidebar.")

elif authentication_status is False:
    st.error('Username/password is incorrect')
elif authentication_status is None:
    st.warning('Please enter your username and password')
