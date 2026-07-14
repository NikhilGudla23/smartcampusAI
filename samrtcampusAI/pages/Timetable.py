import streamlit as st
import pandas as pd
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

st.markdown("<h1>Timetable Scheduler</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #94a3b8;'>View, filter, and plan schedules for academic lectures, tutorials, and lab exams.</p>", unsafe_allow_html=True)

role = st.session_state.role
timetable = load_json("timetable")

# Sidebar Filters
st.sidebar.subheader("Schedule Filter")
dept_filter = st.sidebar.selectbox("Department", ["Computer Science", "Electronics", "Mathematics"])
day_filter = st.sidebar.selectbox("Day of Week", ["All", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])

# Apply filters
filtered_schedule = [t for t in timetable if t.get("department") == dept_filter]
if day_filter != "All":
    filtered_schedule = [t for t in filtered_schedule if t.get("day") == day_filter]

# Render layout
if role == "Faculty":
    tab_view, tab_schedule = st.tabs(["⏰ Lecture Timetable", "➕ Add Timetable Slot"])
else:
    tab_view = st.container()

with tab_view:
    st.markdown(f"### Lectures for {dept_filter} ({day_filter if day_filter != 'All' else 'Full Week'})")
    if not filtered_schedule:
        st.info("No lecture schedules logged matching this selection.")
    else:
        df_schedule = pd.DataFrame(filtered_schedule)
        
        # Sort by day name index
        day_order = {"Monday": 1, "Tuesday": 2, "Wednesday": 3, "Thursday": 4, "Friday": 5}
        df_schedule["day_idx"] = df_schedule["day"].map(day_order)
        df_schedule = df_schedule.sort_values(by=["day_idx", "time"])
        
        df_show = df_schedule[["day", "time", "subject", "room", "faculty"]].copy()
        df_show.columns = ["Day", "Timing Slot", "Subject Name", "Room / Laboratory", "Instructor"]
        
        st.dataframe(df_show, use_container_width=True, hide_index=True)

if role == "Faculty":
    with tab_schedule:
        st.markdown("### Create New Lecture Slot")
        with st.container(border=True):
            slot_dept = st.selectbox("Assign Department", ["Computer Science", "Electronics", "Mathematics"], key="slot_dept")
            slot_day = st.selectbox("Lecture Day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
            slot_subject = st.selectbox("Select Subject", ["Advanced AI", "Cloud Computing", "Signal Processing", "Algorithms", "Linear Algebra", "Calculus"])
            
            # Text inputs for time and room
            slot_time = st.text_input("Timing Slot", placeholder="e.g. 09:00 AM - 10:30 AM")
            slot_room = st.text_input("Room / Lab Name", placeholder="e.g. Room 402, Lab 1")
            
            # Faculty name auto-filled or override
            slot_faculty = st.text_input("Assigning Faculty", value=st.session_state.name)
            
            if st.button("Schedule Slot", use_container_width=True, type="primary"):
                if not slot_time or not slot_room or not slot_faculty:
                    st.error("Please fill in all details.")
                else:
                    new_slot = {
                        "id": f"t_{len(timetable) + 1}",
                        "department": slot_dept,
                        "day": slot_day,
                        "subject": slot_subject,
                        "time": slot_time,
                        "room": slot_room,
                        "faculty": slot_faculty
                    }
                    
                    timetable.append(new_slot)
                    if save_json("timetable", timetable):
                        st.success(f"Timetable slot successfully scheduled for {slot_subject} on {slot_day}!")
                        st.rerun()
                    else:
                        st.error("Failed to save timetable slot.")
            
            st.markdown("""
            > [!TIP]
            > Ensure timing slots do not conflict with existing department rooms and lectures to prevent scheduling overlaps.
            """, unsafe_allow_html=True)
