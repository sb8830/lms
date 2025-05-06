import streamlit as st
import pandas as pd

# ---- Simulated Database ----
users = {}
courses = [
    {"title": "Basics of Stock Market", "level": "Beginner"},
    {"title": "Technical Analysis", "level": "Intermediate"},
    {"title": "Options Trading", "level": "Advanced"},
]

# ---- Session State Init ----
if "user" not in st.session_state:
    st.session_state.user = None
if "enrolled_courses" not in st.session_state:
    st.session_state.enrolled_courses = []

# ---- Pages ----
def home():
    st.title("📈 Welcome to FinEdu LMS")
    st.subheader("Learn the Stock Market with Our Experts")
    st.markdown("Navigate to the sidebar to Login or Explore Courses.")

def login():
    st.subheader("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in users and users[username] == password:
            st.session_state.user = username
            st.success(f"Welcome back, {username}!")
        else:
            st.error("Invalid credentials.")

def register():
    st.subheader("🧾 Register")
    username = st.text_input("Create Username")
    password = st.text_input("Create Password", type="password")
    if st.button("Register"):
        if username in users:
            st.warning("User already exists.")
        else:
            users[username] = password
            st.success("Registration successful. Please login.")

def catalog():
    st.subheader("📚 Course Catalog")
    for course in courses:
        st.markdown(f"**{course['title']}** — *{course['level']}*")
        if st.session_state.user:
            if st.button(f"Enroll in {course['title']}", key=course['title']):
                if course['title'] not in st.session_state.enrolled_courses:
                    st.session_state.enrolled_courses.append(course['title'])
                    st.success(f"Enrolled in {course['title']}!")
                else:
                    st.info("Already enrolled.")
        else:
            st.info("Login to enroll.")

def dashboard():
    st.subheader(f"📊 Dashboard - {st.session_state.user}")
    if st.session_state.enrolled_courses:
        st.markdown("### Your Courses:")
        for course in st.session_state.enrolled_courses:
            st.markdown(f"- {course}")
    else:
        st.info("You haven't enrolled in any courses yet.")

def stock_data():
    st.subheader("📉 Market Data (Mock)")
    st.markdown("Live stock data will be integrated here via an API like Alpha Vantage or Yahoo Finance.")

def admin_panel():
    st.subheader("🛠️ Admin Panel (Demo)")
    st.text("Add course functionality can be implemented here.")
    new_course = st.text_input("Course Title")
    new_level = st.selectbox("Level", ["Beginner", "Intermediate", "Advanced"])
    if st.button("Add Course"):
        courses.append({"title": new_course, "level": new_level})
        st.success("Course added.")

# ---- Sidebar ----
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Go to", ["Home", "Login", "Register", "Catalog", "Dashboard", "Market", "Admin"])

# ---- Routing ----
if page == "Home":
    home()
elif page == "Login":
    login()
elif page == "Register":
    register()
elif page == "Catalog":
    catalog()
elif page == "Dashboard":
    if st.session_state.user:
        dashboard()
    else:
        st.warning("Please login first.")
elif page == "Market":
    stock_data()
elif page == "Admin":
    admin_panel()
