import streamlit as st
import pyrebase
import json
from google.cloud import firestore

# Load Firebase config
with open("firebase_config.json") as f:
    firebase_config = json.load(f)

# Initialize Firebase
firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
db = firestore.Client.from_service_account_info(firebase_config)

# Set Streamlit page config
st.set_page_config(page_title="FinEdu LMS", layout="wide")

# Session state
if "user" not in st.session_state:
    st.session_state.user = None
if "role" not in st.session_state:
    st.session_state.role = None

# ----------------------------
# Authentication functions
# ----------------------------
def login():
    st.subheader("🔐 Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            st.session_state.user = email
            if email == "admin@finedu.com":
                st.session_state.role = "admin"
            else:
                st.session_state.role = "student"
            st.success(f"Welcome, {email}!")
        except:
            st.error("Login failed. Check credentials.")

def register():
    st.subheader("📝 Register")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        try:
            user = auth.create_user_with_email_and_password(email, password)
            db.collection("users").document(email).set({"role": "student"})
            st.success("Registered successfully! Please login.")
        except:
            st.error("Registration failed.")

# ----------------------------
# Public Website
# ----------------------------
def website_home():
    st.title("📈 Welcome to FinEdu")
    st.markdown("Learn the stock market from experts.")
    st.image("https://images.unsplash.com/photo-1559526324-593bc073d938", use_column_width=True)

def website_about():
    st.header("About Us")
    st.write("We are a financial education platform focused on the Indian stock market.")

def website_contact():
    st.header("Contact Us")
    st.write("📧 support@finedu.com")
    st.write("📍 Mumbai, India")

# ----------------------------
# LMS Portal
# ----------------------------
def lms_dashboard():
    st.title("🎓 LMS Dashboard")
    email = st.session_state.user
    user_doc = db.collection("users").document(email).get()
    enrolled = user_doc.to_dict().get("enrolled_courses", [])
    if enrolled:
        st.subheader("Your Courses:")
        for course in enrolled:
            st.markdown(f"- {course}")
    else:
        st.info("You haven't enrolled in any courses.")

def lms_catalog():
    st.subheader("📚 Course Catalog")
    courses = db.collection("courses").stream()
    for c in courses:
        course = c.to_dict()
        st.markdown(f"**{course['title']}** — *{course['level']}*")
        if st.button(f"Enroll in {course['title']}", key=course['title']):
            user_ref = db.collection("users").document(st.session_state.user)
            user_doc = user_ref.get().to_dict()
            enrolled = user_doc.get("enrolled_courses", [])
            if course['title'] not in enrolled:
                enrolled.append(course['title'])
                user_ref.update({"enrolled_courses": enrolled})
                st.success(f"Enrolled in {course['title']}")
            else:
                st.info("Already enrolled.")

# ----------------------------
# Admin Panel
# ----------------------------
def admin_dashboard():
    st.title("🛠️ Admin Panel")
    st.markdown("## 🔗 Portal Links")
    base_url = st.experimental_get_url().split("?")[0]
    st.markdown(f"- 🌐 Website: [{base_url}?page=website]({base_url}?page=website)")
    st.markdown(f"- 🎓 LMS: [{base_url}?page=lms]({base_url}?page=lms)")
    st.markdown(f"- 🔐 Admin Panel: [{base_url}]({base_url})")

    st.markdown("## ➕ Add New Course")
    title = st.text_input("Course Title")
    level = st.selectbox("Level", ["Beginner", "Intermediate", "Advanced"])
    if st.button("Add Course"):
        db.collection("courses").document(title).set({
            "title": title,
            "level": level
        })
        st.success("Course added.")

    st.markdown("## 📋 Existing Courses")
    courses = db.collection("courses").stream()
    for course in courses:
        data = course.to_dict()
        st.markdown(f"- **{data['title']}** ({data['level']})")

# ----------------------------
# Page Routing
# ----------------------------
query_params = st.experimental_get_query_params()
page = query_params.get("page", ["admin"])[0]

if page == "website":
    section = st.sidebar.radio("Website Pages", ["Home", "About", "Contact"])
    if section == "Home":
        website_home()
    elif section == "About":
        website_about()
    elif section == "Contact":
        website_contact()

elif page == "lms":
    if not st.session_state.user or st.session_state.role != "student":
        login_or_register = st.sidebar.radio("Choose", ["Login", "Register"])
        if login_or_register == "Login":
            login()
        else:
            register()
    else:
        section = st.sidebar.radio("LMS", ["Dashboard", "Course Catalog"])
        if section == "Dashboard":
            lms_dashboard()
        elif section == "Course Catalog":
            lms_catalog()

else:  # Admin Panel
    if not st.session_state.user or st.session_state.role != "admin":
        login()
    else:
        admin_dashboard()
