import streamlit as st
import config
from utils.database import seed_database
from utils.helpers import inject_custom_css, get_hero_html, get_feature_card_html

# Set Page Config
st.set_page_config(
    page_title=config.APP_NAME,
    page_icon=config.APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Database on boot
seed_database()

# Initialize Session State
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = None
if "role" not in st.session_state:
    st.session_state.role = None
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

# Inject Custom CSS & Style sheets
inject_custom_css()

# Define st.Page objects for navigation
login_page = st.Page("pages/Login.py", title="Sign In", icon="🔒")
register_page = st.Page("pages/Register.py", title="Create Account", icon="📝")
dashboard_page = st.Page("pages/Dashboard.py", title="Dashboard", icon="📊")
student_page = st.Page("pages/Student.py", title="Students Profile", icon="👥")
faculty_page = st.Page("pages/Faculty.py", title="Faculty Contacts", icon="👨‍🏫")
attendance_page = st.Page("pages/Attendance.py", title="Attendance Log", icon="📅")
library_page = st.Page("pages/Library.py", title="Library Center", icon="📚")
timetable_page = st.Page("pages/Timetable.py", title="Timetable Grid", icon="⏰")
assignments_page = st.Page("pages/Assignments.py", title="Assignments Portal", icon="📝")
notifications_page = st.Page("pages/Notifications.py", title="System Alerts", icon="🔔")
ai_assistant_page = st.Page("pages/AI_Assistant.py", title="Gemini Assistant", icon="💬")
settings_page = st.Page("pages/Settings.py", title="Settings Dashboard", icon="⚙️")

# Custom landing page function
def render_landing():
    # Toggle theme helper in Landing Page
    col_t1, col_t2 = st.columns([10, 1])
    with col_t2:
        current_theme = st.session_state.get("theme", "dark")
        btn_label = "☀️ Light" if current_theme == "dark" else "🌙 Dark"
        if st.button(btn_label, key="theme_toggle_landing"):
            st.session_state.theme = "light" if current_theme == "dark" else "dark"
            st.rerun()
            
    # Draw Navbar HTML
    st.markdown(f"""
    <div class="nav-bar">
        <div class="nav-logo">
            <span>{config.APP_ICON}</span> {config.APP_NAME}
        </div>
        <div class="nav-links">
            <a class="nav-link" href="#features">Features</a>
            <a class="nav-link" href="#pricing">Pricing</a>
            <a class="nav-link" href="#about">About</a>
            <a class="nav-link" href="#contact">Contact</a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Draw Hero HTML
    st.markdown(get_hero_html(), unsafe_allow_html=True)
    
    # CTA Buttons
    col_c1, col_c2, col_c3, col_c4 = st.columns([1, 1, 1, 1])
    with col_c1:
        if st.button("🚀 Get Started", use_container_width=True, key="get_started_btn"):
            st.switch_page(register_page)
    with col_c2:
        if st.button("🔑 Sign In Portal", use_container_width=True, key="signin_btn"):
            st.switch_page(login_page)
    with col_c3:
        if st.button("🌐 Live Demo Info", use_container_width=True, key="demo_btn"):
            st.toast("Welcome! You can log in using student@smartcampus.edu or faculty@smartcampus.edu with Password123.", icon="💡")
    with col_c4:
        if st.button("📖 Documentation", use_container_width=True, key="docs_btn"):
            st.info("System architecture: Streamlit frontend + Thread-locked local JSON records + Google Gemini conversational core.")
            
    st.markdown("<br><hr style='border-color: rgba(255,255,255,0.05);' id='features'><br>", unsafe_allow_html=True)
    
    # Feature Cards Section
    st.markdown("<h2 style='text-align: center; margin-bottom: 30px;'>Core Capabilities</h2>", unsafe_allow_html=True)
    
    f1, f2, f3 = st.columns(3)
    with f1:
        st.markdown(get_feature_card_html("Student Management", "Comprehensive student profile tracking, grading lists, and records.", "👥"), unsafe_allow_html=True)
        st.markdown(get_feature_card_html("Assignments Desk", "Upload, review, grade tasks, and submit files seamlessly.", "📝"), unsafe_allow_html=True)
    with f2:
        st.markdown(get_feature_card_html("AI Assistant", "Conversational chatbot powered by Google Gemini to resolve course topics and codes.", "💬"), unsafe_allow_html=True)
        st.markdown(get_feature_card_html("Library Catalog", "Interactive index of textbooks, availability logs, and reservation schedules.", "📚"), unsafe_allow_html=True)
    with f3:
        st.markdown(get_feature_card_html("Attendance Control", "Faculty portal to mark attendance and student portal to track history.", "📅"), unsafe_allow_html=True)
        st.markdown(get_feature_card_html("Timetable Scheduler", "Visual calendar grids displaying subject slots and room codes.", "⏰"), unsafe_allow_html=True)

    # Pricing & Info Footer
    st.markdown("<br><hr style='border-color: rgba(255,255,255,0.05);' id='pricing'><br>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>Pricing Plans</h2>", unsafe_allow_html=True)
    
    p1, p2, p3 = st.columns(3)
    with p1:
        st.markdown("""
        <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); border-radius: 16px; padding: 25px; text-align: center;">
            <h3>Basic</h3>
            <p style="font-size: 1.8rem; font-weight: 700;">Free</p>
            <p>For small schools & classrooms</p>
            <hr style="border-color: rgba(255,255,255,0.05);">
            <ul style="text-align: left; font-size: 0.9rem; list-style-type: '✓ '; padding-left: 15px;">
                <li>Up to 100 Students</li>
                <li>Basic Analytics</li>
                <li>Standard Library Log</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with p2:
        st.markdown("""
        <div style="background: rgba(99,102,241,0.05); border: 2px solid rgba(99,102,241,0.3); border-radius: 16px; padding: 25px; text-align: center; transform: scale(1.03);">
            <span style="background: #6366f1; color: white; padding: 2px 10px; border-radius: 10px; font-size: 0.75rem; font-weight: 600;">POPULAR</span>
            <h3>Enterprise</h3>
            <p style="font-size: 1.8rem; font-weight: 700;">Custom</p>
            <p>For complete university platforms</p>
            <hr style="border-color: rgba(99,102,241,0.2);">
            <ul style="text-align: left; font-size: 0.9rem; list-style-type: '✓ '; padding-left: 15px;">
                <li>Unlimited Students & Staff</li>
                <li>Complete Gemini AI Assistant</li>
                <li>Advanced Attendance Log</li>
                <li>Custom Portal Hosting</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with p3:
        st.markdown("""
        <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); border-radius: 16px; padding: 25px; text-align: center;">
            <h3>Standard</h3>
            <p style="font-size: 1.8rem; font-weight: 700;">$99/mo</p>
            <p>For colleges & departments</p>
            <hr style="border-color: rgba(255,255,255,0.05);">
            <ul style="text-align: left; font-size: 0.9rem; list-style-type: '✓ '; padding-left: 15px;">
                <li>Up to 1000 Students</li>
                <li>Timetabling & Notification</li>
                <li>Dedicated File Desk</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# Define welcome page object
home_page = st.Page(render_landing, title="Welcome", icon="🏫")

# Navigation Controller based on Session State
if not st.session_state.logged_in:
    # Unauthenticated routes
    pg = st.navigation({
        "Gateway": [home_page, login_page, register_page]
    })
else:
    # Authenticated role-based routes
    role = st.session_state.role
    
    # Common pages
    main_pages = [
        dashboard_page,
        ai_assistant_page,
        attendance_page,
        timetable_page,
        assignments_page,
        library_page,
        notifications_page,
        student_page,
        faculty_page,
        settings_page
    ]
    
    pg = st.navigation({
        "SmartCampusAI": main_pages
    })

# Run Navigation
pg.run()
