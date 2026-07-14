import streamlit as st
from utils.database import load_json
from utils.helpers import inject_custom_css, card_wrapper

# Gating
if not st.session_state.get("logged_in", False):
    st.warning("Please sign in to access this page.")
    st.switch_page("pages/Login.py")
    st.stop()

# Styling
inject_custom_css()
theme = st.session_state.theme

st.markdown("<h1>Faculty Directory</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #94a3b8;'>Connect with course instructors, research advisors, and administrative staff.</p>", unsafe_allow_html=True)

# Load users and filter faculty
users = load_json("users")
faculty_list = [u for u in users if u.get("role") == "Faculty"]

# Sidebar filters
st.sidebar.subheader("Filters")
search_query = st.sidebar.text_input("Search Faculty by Name", "").strip().lower()
dept_filter = st.sidebar.selectbox("Department", ["All", "Computer Science", "Electronics", "Mathematics"])

# Apply filters
filtered_faculty = faculty_list
if search_query:
    filtered_faculty = [f for f in filtered_faculty if search_query in f.get("name", "").lower()]
if dept_filter != "All":
    filtered_faculty = [f for f in filtered_faculty if f.get("department") == dept_filter]

if not filtered_faculty:
    st.info("No faculty members found matching your search.")
else:
    # Display as a grid of contact cards
    cols = st.columns(2)
    for index, f in enumerate(filtered_faculty):
        col = cols[index % 2]
        
        # Designations based on name (simulated)
        designation = "Senior Lecturer"
        if "Dr." in f.get("name", ""):
            designation = "Associate Professor"
        elif "Prof." in f.get("name", ""):
            designation = "Professor & Chairperson"
            
        contact_html = f"""
        <div style="margin-bottom: 10px;">
            <p style="margin: 0; font-size: 0.95rem; color: #a855f7; font-weight: 600;">{designation}</p>
            <p style="margin: 5px 0; font-size: 0.9rem;"><b>Dept:</b> {f.get("department")}</p>
            <p style="margin: 5px 0; font-size: 0.9rem;"><b>📧 Email:</b> <a href="mailto:{f.get("email")}" style="color: #6366f1; text-decoration: none;">{f.get("email")}</a></p>
            <p style="margin: 5px 0; font-size: 0.9rem;"><b>📞 Mobile:</b> {f.get("mobile", "N/A")}</p>
            <p style="margin: 5px 0; font-size: 0.9rem;"><b>⏰ Office Hours:</b> Mon/Wed 02:00 PM - 04:00 PM</p>
        </div>
        """
        
        with col:
            st.markdown(card_wrapper(f.get("name"), contact_html, "👨‍🏫", theme), unsafe_allow_html=True)
            
    # Add a CTA to request support
    st.markdown("---")
    st.markdown("### Academic Counseling Support")
    with st.container(border=True):
        st.markdown("""
        Need academic counseling or thesis discussion guidance? 
        You can schedule a virtual meeting slots directly by emailing the department coordinates above or use the AI Assistant for general topics resolution.
        """)
        if st.button("💬 Ask AI Assistant for Study Tips", use_container_width=True):
            st.switch_page("pages/AI_Assistant.py")
