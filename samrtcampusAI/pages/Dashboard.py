import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from utils.database import load_json
from utils.helpers import inject_custom_css, glass_metric, card_wrapper

# Gating access
if not st.session_state.get("logged_in", False):
    st.warning("Please sign in to access this page.")
    st.switch_page("pages/Login.py")
    st.stop()

# Styling
inject_custom_css()

# Sidebar User Section & Logout Button
st.sidebar.markdown(f"""
<div style="text-align: center; padding: 15px 0;">
    <div style="font-size: 3rem;">👤</div>
    <h4 style="margin: 10px 0 2px 0; color: white;">{st.session_state.name}</h4>
    <p style="color: #6366f1; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; margin: 0;">{st.session_state.role}</p>
</div>
""", unsafe_allow_html=True)

if st.sidebar.button("🚪 Logout Session", use_container_width=True, type="secondary"):
    from utils.auth import logout_user
    logout_user()

# Theme toggle in sidebar
current_theme = st.session_state.get("theme", "dark")
st.sidebar.markdown("---")
st.sidebar.subheader("Preferences")
if st.sidebar.button("☀️ Light Theme" if current_theme == "dark" else "🌙 Dark Theme", use_container_width=True, key="theme_toggle_dash"):
    st.session_state.theme = "light" if current_theme == "dark" else "dark"
    st.rerun()

# Dashboard Title
st.markdown(f"<h1>Dashboard Overview</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='color: #94a3b8;'>Welcome back, {st.session_state.name}. Here is what is happening at the campus today.</p>", unsafe_allow_html=True)

# Fetch data for metrics
users = load_json("users")
students = load_json("students")
attendance = load_json("attendance")
assignments = load_json("assignments")
library = load_json("library")
notifications = load_json("notifications")

# Filter notifications based on role
user_email = st.session_state.email
role = st.session_state.role
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

total_students = len(students)
total_faculty = sum(1 for u in users if u.get("role") == "Faculty")

# Attendance rate computation
today_str = datetime.now().strftime("%Y-%m-%d")
today_att = [a for a in attendance if a.get("date") == today_str]
if today_att:
    present = sum(1 for a in today_att if a.get("status") == "Present")
    attendance_rate = f"{int((present / len(today_att)) * 100)}%"
else:
    # Use global average rate of seeded student data
    avg_rate = sum(s.get("attendance_rate", 0) for s in students) / len(students) if students else 0
    attendance_rate = f"{avg_rate:.1f}%"

total_assignments = len(assignments)
borrowed_books = sum(1 for b in library if b.get("status") == "Borrowed")
alert_count = len(relevant_notifs)

# Metrics Grid (HTML custom render for Glassmorphism cards)
m1, m2, m3, m4, m5, m6 = st.columns(6)
theme = st.session_state.theme

with m1:
    st.markdown(glass_metric("Students", f"{total_students}", "👥", theme), unsafe_allow_html=True)
with m2:
    st.markdown(glass_metric("Faculty", f"{total_faculty}", "👨‍🏫", theme), unsafe_allow_html=True)
with m3:
    st.markdown(glass_metric("Attendance", attendance_rate, "📅", theme), unsafe_allow_html=True)
with m4:
    st.markdown(glass_metric("Assignments", f"{total_assignments}", "📝", theme), unsafe_allow_html=True)
with m5:
    st.markdown(glass_metric("Borrowed Books", f"{borrowed_books}", "📚", theme), unsafe_allow_html=True)
with m6:
    st.markdown(glass_metric("Unread Alerts", f"{alert_count}", "🔔", theme), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Layout: Two columns for key charts
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    # 1. Attendance Trend Over Time
    df_att = pd.DataFrame(attendance)
    if not df_att.empty:
        # Group by date and calculate percentage of present status
        df_att["is_present"] = df_att["status"].apply(lambda x: 1 if x == "Present" else 0)
        trend = df_att.groupby("date").agg(
            total=("is_present", "count"),
            present=("is_present", "sum")
        ).reset_index()
        trend["Percentage"] = (trend["present"] / trend["total"]) * 100
        # Sort by date
        trend = trend.sort_values("date")
        
        fig_trend = px.line(
            trend, 
            x="date", 
            y="Percentage",
            title="Average Attendance Rate Trend (%)",
            labels={"Percentage": "Attendance Rate (%)", "date": "Date"},
            markers=True
        )
        # Custom premium chart styles
        fig_trend.update_traces(line_color="#6366f1", line_width=3, marker=dict(size=8, color="#ec4899"))
        fig_trend.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#94a3b8",
            xaxis=dict(showgrid=False),
            yaxis=dict(gridcolor="rgba(255,255,255,0.05)", range=[60, 105])
        )
        st.plotly_chart(fig_trend, use_container_width=True)
    else:
        st.info("No attendance trend data available.")

with col_chart2:
    # 2. Department-wise Student distribution
    df_stud = pd.DataFrame(students)
    if not df_stud.empty:
        dept_counts = df_stud["department"].value_counts().reset_index()
        dept_counts.columns = ["Department", "Students"]
        
        fig_pie = px.pie(
            dept_counts,
            names="Department",
            values="Students",
            title="Student Distribution by Department",
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_pie.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            legend_font_color="#94a3b8",
            title_font_color="#f8fafc" if theme == "dark" else "#1e293b",
            font_color="#94a3b8"
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("No student records found.")

# Layout: Activity Log and Quick Actions
col_actions, col_logs = st.columns([1, 2])

with col_actions:
    action_content = f"""
    <div style="display: flex; flex-direction: column; gap: 10px;">
        <p style="font-size: 0.95rem; margin-bottom: 15px;">Choose from these smart action paths to work inside the portal:</p>
    </div>
    """
    st.markdown(card_wrapper("Quick Operations", action_content, "⚡", theme), unsafe_allow_html=True)
    
    if st.button("💬 Chat with Gemini Copilot", use_container_width=True):
        st.switch_page("pages/AI_Assistant.py")
    if st.button("📅 Mark/Review Attendance", use_container_width=True):
        st.switch_page("pages/Attendance.py")
    if st.button("📝 Assignments Portal", use_container_width=True):
        st.switch_page("pages/Assignments.py")
    if st.button("⚙️ User Settings", use_container_width=True):
        st.switch_page("pages/Settings.py")

with col_logs:
    # List the 3 most recent notifications (filtered)
    notifications_sorted = sorted(relevant_notifs, key=lambda x: x.get("date", ""), reverse=True)
    recent_notifs = notifications_sorted[:3]
    
    notif_list_html = ""
    for n in recent_notifs:
        badge_color = "#3b82f6"  # system blue
        if n.get("type") == "Exam":
            badge_color = "#ef4444"
        elif n.get("type") == "Assignment":
            badge_color = "#f59e0b"
            
        title_color = '#f8fafc' if theme == 'dark' else '#1e293b'
        msg_color = '#94a3b8' if theme == 'dark' else '#475569'
        
        item_html = (
            f"<div style='border-bottom: 1px solid rgba(255,255,255,0.05); padding: 12px 0;'>"
            f"<div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;'>"
            f"<span style='font-weight: 600; font-size: 1rem; color: {title_color};'>{n.get('title')}</span>"
            f"<span style='background: {badge_color}; color: white; font-size: 0.75rem; padding: 2px 8px; border-radius: 8px; font-weight: 600;'>{n.get('type')}</span>"
            f"</div>"
            f"<p style='margin: 0 0 4px 0; font-size: 0.9rem; color: {msg_color};'>{n.get('message')}</p>"
            f"<small style='color: #6366f1; font-size: 0.8rem;'>{n.get('date')}</small>"
            f"</div>"
        )
        notif_list_html += item_html
        
    st.markdown(card_wrapper("Recent Announcements & Updates", notif_list_html or "<p style='margin:0;'>No recent alerts.</p>", "🔔", theme), unsafe_allow_html=True)
