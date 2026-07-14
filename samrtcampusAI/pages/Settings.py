import streamlit as st
from utils.database import load_json, update_json
from utils.security import hash_password, verify_password, validate_password_strength
from utils.helpers import inject_custom_css, card_wrapper
from utils.ai import check_api_status

# Gating
if not st.session_state.get("logged_in", False):
    st.warning("Please sign in to access this page.")
    st.switch_page("pages/Login.py")
    st.stop()

# Styling
inject_custom_css()
theme = st.session_state.theme

st.markdown("<h1>Settings Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #94a3b8;'>Manage your student/faculty profile, account credentials, and platform integration preferences.</p>", unsafe_allow_html=True)

user = st.session_state.user

tab_profile, tab_security, tab_system, tab_api = st.tabs([
    "👤 Profile Details", 
    "🔒 Security & Credentials", 
    "⚙️ Preferences", 
    "🔌 Integrations Status"
])

# 1. PROFILE DETAILS
with tab_profile:
    st.markdown("### Profile Information")
    with st.container(border=True):
        st.markdown(f"**Name:** {user.get('name')}")
        st.markdown(f"**Email:** {user.get('email')}")
        st.markdown(f"**Role:** {user.get('role')}")
        st.markdown(f"**Department:** {user.get('department')}")
        if user.get("role") == "Student":
            st.markdown(f"**Student ID:** {user.get('student_id')}")
            
        st.markdown("---")
        st.markdown("#### Update Contact Details")
        new_mobile = st.text_input("Mobile Number", value=user.get("mobile", ""))
        
        if st.button("Save Profile Updates", type="primary"):
            if update_json("users", user.get("id"), {"mobile": new_mobile}):
                # Refresh session state user
                users_db = load_json("users")
                st.session_state.user = next((u for u in users_db if u.get("id") == user.get("id")), None)
                st.success("Profile contact details successfully updated!")
                st.rerun()
            else:
                st.error("Failed to update contact details.")

# 2. SECURITY & PASSWORD
with tab_security:
    st.markdown("### Change Account Password")
    with st.container(border=True):
        old_pass = st.text_input("Current Password", type="password", key="old_pass")
        new_pass = st.text_input("New Password", type="password", key="new_pass")
        confirm_pass = st.text_input("Confirm New Password", type="password", key="confirm_pass")
        
        if st.button("Update Password", type="primary"):
            if not old_pass or not new_pass or not confirm_pass:
                st.error("Please fill in all password fields.")
            elif new_pass != confirm_pass:
                st.error("New passwords do not match.")
            else:
                # Verify old password
                if not verify_password(old_pass, user.get("password")):
                    st.error("Incorrect current password.")
                else:
                    # Validate strength
                    is_strong, strength_msg = validate_password_strength(new_pass)
                    if not is_strong:
                        st.error(strength_msg)
                    else:
                        hashed = hash_password(new_pass)
                        if update_json("users", user.get("id"), {"password": hashed}):
                            st.success("Password updated successfully! Please keep it secure.")
                        else:
                            st.error("Failed to update password.")

# 3. SYSTEM PREFERENCES
with tab_system:
    st.markdown("### Platform Configurations")
    with st.container(border=True):
        st.markdown("#### Theme Control")
        current_theme = st.session_state.get("theme", "dark")
        theme_toggle = st.selectbox("Preferred Palette Theme", ["Dark Mode", "Light Mode"], index=0 if current_theme == "dark" else 1)
        
        # Detect change
        theme_val = "dark" if theme_toggle == "Dark Mode" else "light"
        if theme_val != current_theme:
            st.session_state.theme = theme_val
            st.rerun()
            
        st.markdown("---")
        st.markdown("#### Language Configuration")
        st.selectbox("System Language", ["English (US)", "Spanish", "French", "German"])
        
        st.markdown("---")
        st.markdown("#### Notifications Control")
        st.checkbox("Receive Coursework Deadline Reminders", value=True)
        st.checkbox("Receive Daily Attendance Alerts", value=False)
        st.checkbox("Receive Automated AI Tutor Recommendations", value=True)
        
        st.button("Save Preferences", type="secondary")

# 4. INTEGRATIONS STATUS
with tab_api:
    st.markdown("### API Integration & System Endpoints")
    
    # Check current environment key statuses
    status_dict = check_api_status()
    
    status_html = ""
    for api_name, api_status in status_dict.items():
        status_color = "#10b981" if "Available" in api_status or "Active" in api_status or "Configured" in api_status else "#ef4444"
        if "Fallback" in api_status:
            status_color = "#f59e0b"
            
        status_html += f"""
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.05); padding: 12px 0;">
            <span style="font-weight: 600;">{api_name}</span>
            <span style="color: {status_color}; font-weight: 700;">{api_status}</span>
        </div>
        """
        
    st.markdown(card_wrapper("Connected Services", status_html, "🔌", theme), unsafe_allow_html=True)
    
    st.markdown("""
    > [!NOTE]
    > To enable Google Gemini AI functionality or change credentials keys, update the corresponding fields inside the root `.env` file of this project directory.
    """, unsafe_allow_html=True)
