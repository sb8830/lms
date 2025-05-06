import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth, firestore
import json
import os

# Initialize Firebase Admin SDK
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_config.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# User Authentication
def login():
    st.subheader("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        try:
            user = auth.get_user_by_email(email)
            st.session_state['user'] = user.uid
            st.success("Logged in successfully!")
        except:
            st.error("Invalid credentials")

def logout():
    st.session_state.pop('user', None)
    st.success("Logged out successfully!")

# Main Application
def main():
    st.title("FinEdu LMS")

    # Navigation
    page = st.sidebar.selectbox("Navigate", ["Website", "LMS Portal", "Admin Panel"])

    if 'user' not in st.session_state:
        login()
    else:
        st.sidebar.button("Logout", on_click=logout)
        if page == "Website":
            st.subheader("Welcome to FinEdu!")
            st.write("This is the public website.")
        elif page == "LMS Portal":
            st.subheader("LMS Portal")
            st.write("Access your courses here.")
        elif page == "Admin Panel":
            st.subheader("Admin Panel")
            st.write("Manage the platform here.")

if __name__ == "__main__":
    main()
