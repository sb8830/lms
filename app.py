import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# Load configuration from YAML file
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Create an authentication object
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# Render the login widget
name, authentication_status, username = authenticator.login('Login', 'main')

# Registration section
if authentication_status is None:
    try:
        email, username, name = authenticator.register_user(pre_authorized=config['preauthorized']['emails'])
        if email:
            st.success('User registered successfully')
            # Update the config.yaml file to remove the registered email from preauthorized list
            config['credentials']['usernames'][username] = {
                'email': email,
                'name': name,
                'password': '',  # The password will be hashed and added automatically
                'role': 'customer'  # Assign a default role or modify as needed
            }
            config['preauthorized']['emails'].remove(email)
            with open('config.yaml', 'w') as file:
                yaml.dump(config, file, default_flow_style=False)
    except Exception as e:
        st.error(e)
