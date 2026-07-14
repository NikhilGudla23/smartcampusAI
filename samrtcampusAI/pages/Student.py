import streamlit as st
import pandas as pd
from utils.database import load_json, save_json, update_json, delete_json
from utils.helpers import inject_custom_css, card_wrapper

# Gating
if not st.session_state.get("logged_in", False):
    st.warning("Please sign in to access this page.")
    st.switch_page("pages/Login.py")
    st.stop()

# Styling
inject_custom_css()
theme = st.session_state.theme

st.markdown("<h1>Student Management</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #94a3b8;'>Review, search, and manage student enrollment and performance profiles.</p>", unsafe_allow_html=True)

role = st.session_state.role

# Load current students list
students = load_json("students")

# Layout: Sidebar filters
st.sidebar.subheader("Filters")
search_query = st.sidebar.text_input("Search by Name or ID", "").strip().lower()
departments = ["All", "Computer Science", "Electronics", "Mathematics", "Mechanical Engineering", "Business Admin"]
dept_filter = st.sidebar.selectbox("Filter by Department", departments)

# Apply filters
filtered_students = students
if search_query:
    filtered_students = [
        s for s in filtered_students
        if search_query in s.get("name", "").lower() or search_query in s.get("student_id", "").lower()
    ]
if dept_filter != "All":
    filtered_students = [s for s in filtered_students if s.get("department") == dept_filter]

# Render Tabs
if role == "Faculty":
    tab_list, tab_add = st.tabs(["👥 Student Directory", "➕ Add New Student"])
else:
    tab_list = st.container()

with tab_list:
    st.markdown("### Enrolled Students")
    if not filtered_students:
        st.info("No students match the criteria.")
    else:
        # Convert to Pandas DataFrame for a clean view
        df_students = pd.DataFrame(filtered_students)
        # Reorder and format columns
        columns_to_show = ["student_id", "name", "email", "department", "cgpa", "attendance_rate", "completed_assignments"]
        df_show = df_students[columns_to_show].copy()
        df_show.columns = ["ID", "Full Name", "Email Address", "Department", "CGPA", "Attendance (%)", "Completed Assignments"]
        
        st.dataframe(df_show, use_container_width=True, hide_index=True)

        # Faculty CRUD Actions: Edit and Delete
        if role == "Faculty":
            st.markdown("---")
            st.markdown("### Manage Records")
            selected_student_id = st.selectbox("Select Student by ID to Edit or Remove", [s.get("student_id") for s in filtered_students])
            
            target_student = next((s for s in students if s.get("student_id") == selected_student_id), None)
            
            if target_student:
                col_edit, col_del = st.columns(2)
                
                with col_edit:
                    with st.container(border=True):
                        st.markdown("#### Edit Profile Details")
                        new_cgpa = st.number_input("CGPA", min_value=0.0, max_value=4.0, value=float(target_student.get("cgpa", 0.0)), step=0.01)
                        new_att = st.number_input("Attendance Rate (%)", min_value=0.0, max_value=100.0, value=float(target_student.get("attendance_rate", 100.0)), step=0.1)
                        new_completed = st.number_input("Completed Assignments", min_value=0, value=int(target_student.get("completed_assignments", 0)))
                        
                        if st.button("Save Updates", use_container_width=True, type="primary"):
                            update_data = {
                                "cgpa": new_cgpa,
                                "attendance_rate": new_att,
                                "completed_assignments": new_completed
                            }
                            if update_json("students", target_student.get("id"), update_data):
                                st.success("Student profile updated successfully!")
                                time_to_wait = 1.0
                                st.rerun()
                            else:
                                st.error("Failed to update student profile.")
                                
                with col_del:
                    with st.container(border=True):
                        st.markdown("#### Remove Student Account")
                        st.warning(f"Are you sure you want to permanently delete {target_student.get('name')}'s profile from the campus directory?")
                        confirm_delete = st.checkbox("Yes, confirm deletion")
                        
                        if st.button("Delete Record", use_container_width=True, type="secondary"):
                            if confirm_delete:
                                # Delete student profile
                                if delete_json("students", target_student.get("id")):
                                    # Also delete from users table
                                    delete_json("users", target_student.get("id"))
                                    st.success("Student record successfully removed.")
                                    st.rerun()
                                else:
                                    st.error("Failed to delete record.")
                            else:
                                st.error("Please confirm deletion by ticking the confirmation box.")

if role == "Faculty":
    with tab_add:
        st.markdown("### Register a New Student Profile")
        with st.container(border=True):
            new_name = st.text_input("Full Name", placeholder="e.g. Liam Johnson")
            new_email = st.text_input("Email", placeholder="e.g. liam@smartcampus.edu")
            new_id = st.text_input("Student ID Number", placeholder="e.g. CS-2026-902")
            new_dept = st.selectbox("Department", departments[1:], key="add_dept")
            
            col_metrics1, col_metrics2 = st.columns(2)
            with col_metrics1:
                new_cgpa = st.number_input("Starting CGPA", min_value=0.0, max_value=4.0, value=0.0, step=0.01, key="add_cgpa")
            with col_metrics2:
                new_attendance = st.number_input("Starting Attendance (%)", min_value=0.0, max_value=100.0, value=100.0, step=0.1, key="add_att")
                
            new_pass = st.text_input("Initial Password", type="password", placeholder="••••••••")
            
            if st.button("Enroll Student", use_container_width=True, type="primary"):
                if not new_name or not new_email or not new_id or not new_pass:
                    st.error("Please fill in all details.")
                else:
                    # Leverage register_user auth function to keep password hashed and databases synced
                    from utils.auth import register_user
                    
                    success, msg = register_user(
                        name=new_name,
                        email=new_email,
                        password=new_pass,
                        mobile="+1000000000",
                        department=new_dept,
                        student_id=new_id,
                        role="Student"
                    )
                    
                    if success:
                        # Fetch the created student user profile to update cgpa and attendance values
                        users = load_json("users")
                        new_user = next((u for u in users if u.get("email") == new_email), None)
                        if new_user:
                            update_json("students", new_user.get("id"), {
                                "cgpa": new_cgpa,
                                "attendance_rate": new_attendance,
                                "joined_date": pd.Timestamp.now().strftime("%Y-%m-%d")
                            })
                        st.success(f"Success! Enrolled student {new_name}.")
                        st.rerun()
                    else:
                        st.error(msg)
