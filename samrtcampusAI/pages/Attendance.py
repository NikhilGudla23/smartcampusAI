import streamlit as st
import pandas as pd
from datetime import datetime
from utils.database import load_json, save_json
from utils.helpers import inject_custom_css, glass_metric, card_wrapper

# Gating
if not st.session_state.get("logged_in", False):
    st.warning("Please sign in to access this page.")
    st.switch_page("pages/Login.py")
    st.stop()

# Styling
inject_custom_css()
theme = st.session_state.theme

st.markdown("<h1>Attendance Tracking</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #94a3b8;'>Monitor daily lecture attendance records and overall semester attendance metrics.</p>", unsafe_allow_html=True)

role = st.session_state.role
attendance = load_json("attendance")
students = load_json("students")

if role == "Faculty":
    tab_view, tab_mark = st.tabs(["📊 View Logs Directory", "✍️ Mark Daily Attendance"])
    
    with tab_view:
        st.markdown("### Daily Attendance Logs")
        if not attendance:
            st.info("No attendance logs created yet.")
        else:
            df_att = pd.DataFrame(attendance)
            # Filter
            dept_select = st.selectbox("Department", ["All", "Computer Science", "Electronics", "Mathematics"])
            
            filtered_df = df_att
            if dept_select != "All":
                filtered_df = df_att[df_att["department"] == dept_select]
                
            if filtered_df.empty:
                st.info("No records match filter.")
            else:
                st.dataframe(
                    filtered_df[["date", "student_id", "student_name", "subject", "status", "marked_by"]],
                    use_container_width=True,
                    hide_index=True
                )
                
    with tab_mark:
        st.markdown("### Mark Daily Lectures")
        with st.container(border=True):
            # Mark details
            mark_date = st.date_input("Lecture Date", datetime.now())
            mark_subject = st.selectbox("Select Lecture Subject", ["Advanced AI", "Cloud Computing", "Signal Processing", "Algorithms", "Linear Algebra"])
            
            # Select student
            student_options = {s.get("name"): s for s in students}
            selected_student_name = st.selectbox("Select Student Profile", list(student_options.keys()))
            
            mark_status = st.radio("Status", ["Present", "Absent"], horizontal=True)
            
            if st.button("Log Attendance Entry", use_container_width=True, type="primary"):
                target_stud = student_options[selected_student_name]
                
                # Check duplicate
                date_str = mark_date.strftime("%Y-%m-%d")
                duplicate = any(
                    a.get("student_id") == target_stud.get("student_id") and
                    a.get("date") == date_str and
                    a.get("subject") == mark_subject
                    for a in attendance
                )
                
                if duplicate:
                    st.error("An attendance entry already exists for this student, subject, and date.")
                else:
                    new_entry = {
                        "id": f"att_{len(attendance) + 1}",
                        "student_id": target_stud.get("student_id"),
                        "student_name": target_stud.get("name"),
                        "department": target_stud.get("department"),
                        "date": date_str,
                        "subject": mark_subject,
                        "status": mark_status,
                        "marked_by": st.session_state.email
                    }
                    
                    attendance.append(new_entry)
                    if save_json("attendance", attendance):
                        # Re-calculate student's global average attendance rate
                        stud_entries = [a for a in attendance if a.get("student_id") == target_stud.get("student_id")]
                        p_count = sum(1 for a in stud_entries if a.get("status") == "Present")
                        new_rate = round((p_count / len(stud_entries)) * 100, 1) if stud_entries else 100.0
                        
                        from utils.database import update_json
                        update_json("students", target_stud.get("id"), {"attendance_rate": new_rate})
                        
                        st.success(f"Successfully marked {target_stud.get('name')} as {mark_status} for {mark_subject}.")
                        st.rerun()
                    else:
                        st.error("Failed to save entry.")

else:
    # Student View
    student_id = st.session_state.user.get("student_id")
    my_records = [a for a in attendance if a.get("student_id") == student_id]
    
    # Calculate stats
    total_lectures = len(my_records)
    p_lectures = sum(1 for a in my_records if a.get("status") == "Present")
    rate = (p_lectures / total_lectures) * 100 if total_lectures > 0 else 100.0
    
    col_rate, col_warn = st.columns(2)
    with col_rate:
        st.markdown(glass_metric("My Attendance Rate", f"{rate:.1f}%", "📊", theme), unsafe_allow_html=True)
    with col_warn:
        if rate >= 75.0:
            st.success("🟢 Safe Standing: Your attendance is above the university threshold of 75%. Keep it up!")
        else:
            st.error("⚠️ Critical Warning: Your attendance is below 75%. You are at risk of final exam debarment.")
            
    st.markdown("### Lecture History Log")
    if not my_records:
        st.info("No attendance records logged for you yet.")
    else:
        df_my = pd.DataFrame(my_records)
        df_my_show = df_my[["date", "subject", "status", "marked_by"]].copy()
        df_my_show.columns = ["Date", "Subject / Lecture", "Status", "Marked By"]
        st.dataframe(df_my_show, use_container_width=True, hide_index=True)
