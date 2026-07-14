import streamlit as st
import pandas as pd
from datetime import datetime
from utils.database import load_json, save_json
from utils.helpers import inject_custom_css, card_wrapper

# Gating
if not st.session_state.get("logged_in", False):
    st.warning("Please sign in to access this page.")
    st.switch_page("pages/Login.py")
    st.stop()

# Styling
inject_custom_css()
theme = st.session_state.theme

st.markdown("<h1>System Alerts & Notifications</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #94a3b8;'>Stay updated with school announcements, timetabling schedules, and assignment submissions.</p>", unsafe_allow_html=True)

role = st.session_state.role
notifications = load_json("notifications")

# Filter logic
# Students see "All", "Student", or their own email address
# Faculty see "All" or "Faculty"
user_email = st.session_state.email
if role == "Student":
    relevant_notifs = [
        n for n in notifications 
        if n.get("recipient") in ["All", "Student", user_email]
    ]
else:
    relevant_notifs = [
        n for n in notifications 
        if n.get("recipient") in ["All", "Faculty", user_email]
    ]

# Sort by date
relevant_notifs = sorted(relevant_notifs, key=lambda x: x.get("date", ""), reverse=True)

if role == "Faculty":
    tab_feed, tab_post = st.tabs(["🔔 Announcement Feed", "📣 Publish Alert"])
else:
    tab_feed = st.container()

with tab_feed:
    st.markdown("### Active Notifications")
    if not relevant_notifs:
        st.info("No active notifications or announcements.")
    else:
        for n in relevant_notifs:
            badge_color = "#3b82f6"  # Blue
            if n.get("type") == "Exam":
                badge_color = "#ef4444"  # Red
            elif n.get("type") == "Assignment":
                badge_color = "#f59e0b"  # Yellow
                
            msg_color = '#94a3b8' if theme == 'dark' else '#475569'
            content = (
                f"<div style='margin-bottom: 5px;'>"
                f"<div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;'>"
                f"<span style='background: {badge_color}; color: white; font-size: 0.75rem; padding: 2px 8px; border-radius: 8px; font-weight: 600;'>{n.get('type')}</span>"
                f"<span style='color: #6366f1; font-size: 0.8rem; font-weight: 500;'>{n.get('date')}</span>"
                f"</div>"
                f"<p style='font-size: 0.95rem; line-height: 1.5; margin: 0 0 8px 0; color: {msg_color};'>{n.get('message')}</p>"
                f"<small style='color: #94a3b8; display: block;'>Recipient: <b>{n.get('recipient')}</b></small>"
                f"</div>"
            )
            st.markdown(card_wrapper(n.get("title"), content, "🔔", theme), unsafe_allow_html=True)

if role == "Faculty":
    with tab_post:
        st.markdown("### Dispatch Campus Announcement")
        with st.container(border=True):
            n_title = st.text_input("Alert Title", placeholder="e.g. Server Maintenance Slot")
            n_msg = st.text_area("Alert Message Body", placeholder="Describe the announcement in full...")
            
            n_type = st.selectbox("Alert Type / Tag", ["System", "Exam", "Assignment", "Event"])
            n_recip_group = st.selectbox("Recipient Target Group", ["All", "Student", "Faculty", "Specific User Email"])
            
            n_recip = ""
            if n_recip_group == "Specific User Email":
                n_recip = st.text_input("Enter Target Email Address", placeholder="e.g. student@smartcampus.edu").strip()
            else:
                n_recip = n_recip_group
                
            if st.button("Dispatch Notification", use_container_width=True, type="primary"):
                if not n_title or not n_msg or not n_recip:
                    st.error("Please fill in the title, message, and recipient details.")
                else:
                    new_n = {
                        "id": f"n_{len(notifications) + 1}",
                        "title": n_title,
                        "message": n_msg,
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "type": n_type,
                        "recipient": n_recip
                    }
                    
                    notifications.append(new_n)
                    if save_json("notifications", notifications):
                        st.success(f"Announcement '{n_title}' dispatched successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to save announcement.")
