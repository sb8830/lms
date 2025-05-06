import streamlit as st

# --------- Simulated Storage ---------
users = {}  # username -> password
courses = [
    {"title": "Basics of Stock Market", "level": "Beginner"},
    {"title": "Technical Analysis", "level": "Intermediate"},
    {"title": "Options Trading", "level": "Advanced"},
]

# --------- Session State ---------
if "user" not in st.session_state:
    st.session_state.user = None
if "role" not in st.session_state:
    st.session_state.role = None
if "enrolled_courses" not in st.session_state:
    st.session_state.enrolled_courses = []

# --------- Public Website ---------
def website_home():
    st.title("📈 FinEdu - Master the Stock Market")
    st.markdown("Welcome to **FinEdu**, your destination to become a stock market pro.")
    st.markdown("""
    - 🧠 Expert-led Courses  
    - 🔔 Market Alerts (coming soon)  
    - 📚 Free Resources  
    - 👨‍🎓 Join 10,000+ learners!
    """)
    st.image("https://images.unsplash.com/photo-1559526324-593bc073d938", use_column_width=True)

def website_about():
    st.subheader("About Us")
    st.write("FinEdu is an edtech platform focused on financial literacy and market education in India and beyond.")

def website_contact():
    st.subheader("Contact")
    st.write("📧 support@finedu.com")
    st.write("📍 Mumbai, India")

# --------- LMS Portal ---------
def lms_login():
    st.subheader("🔐 LMS Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in users and users[username] == password:
            st.session_state.user = username
            st.session_state.role = "student"
            st.success(f"Welcome, {username}!")
        else:
            st.error("Invalid credentials.")

def lms_register():
    st.subheader("📝 LMS Registration")
    username = st.text_input("Create Username")
    password = st.text_input("Create Password", type="password")
    if st.button("Register"):
        if username in users:
            st.warning("User already exists.")
        else:
            users[username] = password
            st.success("Registration successful! Please login.")

def lms_dashboard():
    st.subheader(f"🎓 {st.session_state.user}'s Dashboard")
    if st.session_state.enrolled_courses:
        st.markdown("### Enrolled Courses:")
        for course in st.session_state.enrolled_courses:
            st.markdown(f"- {course}")
    else:
        st.info("No enrolled courses yet.")
        
def lms_catalog():
    st.subheader("📚 Course Catalog")
    for course in courses:
        st.markdown(f"**{course['title']}** — *{course['level']}*")
        if st.button(f"Enroll in {course['title']}", key=course['title']):
            if course['title'] not in st.session_state.enrolled_courses:
                st.session_state.enrolled_courses.append(course['title'])
                st.success(f"Enrolled in {course['title']}!")
            else:
                st.info("Already enrolled.")

# --------- Admin Control Panel ---------
def admin_login():
    st.subheader("🔐 Admin Login")
    username = st.text_input("Admin Username")
    password = st.text_input("Admin Password", type="password")
    if st.button("Login as Admin"):
        if username == "admin" and password == "admin123":
            st.session_state.user = "admin"
            st.session_state.role = "admin"
            st.success("Admin logged in.")
        else:
            st.error("Invalid admin credentials.")

def admin_dashboard():
    st.subheader("🛠️ Admin Dashboard")
    st.markdown("### Add New Course")
    title = st.text_input("Course Title")
    level = st.selectbox("Level", ["Beginner", "Intermediate", "Advanced"])
    if st.button("Add Course"):
        courses.append({"title": title, "level": level})
        st.success("Course added successfully!")

    st.markdown("### Current Courses")
    for course in courses:
        st.markdown(f"- **{course['title']}** ({course['level']})")

# --------- Navigation Sidebar ---------
st.sidebar.title("🔍 Portal Selection")
portal = st.sidebar.radio("Choose your view", ["Website", "LMS Portal", "Admin Panel"])

# --------- Render Based on Portal ---------
if portal == "Website":
    section = st.sidebar.radio("Pages", ["Home", "About", "Contact"])
    if section == "Home":
        website_home()
    elif section == "About":
        website_about()
    elif section == "Contact":
        website_contact()

elif portal == "LMS Portal":
    section = st.sidebar.radio("LMS Pages", ["Login", "Register", "Dashboard", "Course Catalog"])
    if section == "Login":
        lms_login()
    elif section == "Register":
        lms_register()
    elif section == "Dashboard":
        if st.session_state.user and st.session_state.role == "student":
            lms_dashboard()
        else:
            st.warning("Login as a student to access the dashboard.")
    elif section == "Course Catalog":
        if st.session_state.user and st.session_state.role == "student":
            lms_catalog()
        else:
            st.warning("Please login to enroll in courses.")

elif portal == "Admin Panel":
    if st.session_state.user != "admin":
        admin_login()
    else:
        admin_dashboard()
