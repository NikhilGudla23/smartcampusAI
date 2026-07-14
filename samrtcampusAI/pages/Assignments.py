import streamlit as st
import pandas as pd
from datetime import datetime
from utils.database import load_json, save_json, update_json
from utils.helpers import inject_custom_css, card_wrapper

# Gating
if not st.session_state.get("logged_in", False):
    st.warning("Please sign in to access this page.")
    st.switch_page("pages/Login.py")
    st.stop()

# Styling
inject_custom_css()
theme = st.session_state.theme

st.markdown("<h1>Assignments Portal</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #94a3b8;'>Publish assignments, submit coursework materials, and review academic grade sheets.</p>", unsafe_allow_html=True)

role = st.session_state.role
assignments = load_json("assignments")

if role == "Faculty":
    tab_list, tab_create, tab_grade = st.tabs(["📝 Academic Assignments", "➕ Create Assignment", "🎓 Grade Submissions"])
    
    # 1. VIEW ASSIGNMENTS
    with tab_list:
        st.markdown("### Published Course Assignments")
        if not assignments:
            st.info("No assignments published yet.")
        else:
            for a in assignments:
                sub_count = len(a.get("submissions", []))
                content = f"""
                <div style="margin-bottom: 5px;">
                    <p><b>Subject:</b> {a.get("subject")} | <b>Department:</b> {a.get("department")}</p>
                    <p><b>Description:</b> {a.get("description")}</p>
                    <p><b>Due Date:</b> <span style="color: #ef4444; font-weight:600;">{a.get("due_date")}</span></p>
                    <p><b>Active Submissions:</b> {sub_count} students submitted</p>
                </div>
                """
                st.markdown(card_wrapper(a.get("title"), content, "📋", theme), unsafe_allow_html=True)

    # 2. CREATE ASSIGNMENT
    with tab_create:
        st.markdown("### Publish Coursework Task")
        with st.container(border=True):
            a_title = st.text_input("Assignment Title", placeholder="e.g. Assignment 4: Recurrent Nets")
            a_desc = st.text_area("Task Description", placeholder="Enter full task details and instructions...")
            
            a_dept = st.selectbox("Department Target", ["Computer Science", "Electronics", "Mathematics"])
            a_sub = st.text_input("Subject Course Name", placeholder="e.g. Advanced AI")
            a_date = st.date_input("Coursework Due Date", datetime.now())
            
            if st.button("Publish Coursework", use_container_width=True, type="primary"):
                if not a_title or not a_desc or not a_sub:
                    st.error("Please fill in all details.")
                else:
                    new_a = {
                        "id": f"a{len(assignments) + 1}",
                        "title": a_title,
                        "description": a_desc,
                        "department": a_dept,
                        "subject": a_sub,
                        "due_date": a_date.strftime("%Y-%m-%d"),
                        "created_by": st.session_state.email,
                        "submissions": []
                    }
                    
                    assignments.append(new_a)
                    if save_json("assignments", assignments):
                        # Trigger system notification
                        notifs = load_json("notifications")
                        new_notif = {
                            "id": f"n_{len(notifs) + 1}",
                            "title": f"New Assignment: {a_sub}",
                            "message": f"Dr. Sarah Jenkins has published '{a_title}'. Check details in assignments portal.",
                            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                            "type": "Assignment",
                            "recipient": "Student"
                        }
                        notifs.append(new_notif)
                        save_json("notifications", notifs)
                        
                        st.success(f"Assignment '{a_title}' published to students catalog.")
                        st.rerun()
                    else:
                        st.error("Failed to save assignment.")

    # 3. GRADE SUBMISSIONS
    with tab_grade:
        st.markdown("### Grade Student Submissions")
        if not assignments:
            st.info("No assignments published.")
        else:
            select_a_title = st.selectbox("Choose Published Assignment", [a.get("title") for a in assignments])
            target_a = next((a for a in assignments if a.get("title") == select_a_title), None)
            
            if target_a:
                subs = target_a.get("submissions", [])
                if not subs:
                    st.info("No submissions logged for this assignment yet.")
                else:
                    # Show list of students who submitted
                    df_subs = pd.DataFrame(subs)
                    st.dataframe(
                        df_subs[["student_id", "student_name", "submission_date", "status", "grade"]],
                        use_container_width=True,
                        hide_index=True
                    )
                    
                    # Grade interface
                    st.markdown("---")
                    st.markdown("#### Enter Grades")
                    
                    student_opts = {s.get("student_name"): s for s in subs}
                    select_stud = st.selectbox("Choose Student to Grade", list(student_opts.keys()))
                    target_sub = student_opts[select_stud]
                    
                    grade_marks = st.selectbox("Assign Letter Grade", ["A+", "A", "B+", "B", "C+", "C", "Fail"])
                    
                    if st.button("Publish Grade", use_container_width=True, type="primary"):
                        # Update submission grade
                        for sub in target_a["submissions"]:
                            if sub.get("student_id") == target_sub.get("student_id"):
                                sub["status"] = "Graded"
                                sub["grade"] = grade_marks
                                break
                                
                        if update_json("assignments", target_a.get("id"), {"submissions": target_a["submissions"]}):
                            st.success(f"Published grade '{grade_marks}' for {select_stud}.")
                            st.rerun()
                        else:
                            st.error("Failed to save grade.")

else:
    # Student Views
    tab_tasks, tab_submit = st.tabs(["📋 Academic Tasks", "📤 Submit Coursework"])
    student_id = st.session_state.user.get("student_id")
    student_dept = st.session_state.user.get("department")
    
    # Filter assignments by student's department
    dept_assignments = [a for a in assignments if a.get("department") == student_dept]
    
    with tab_tasks:
        st.markdown("### Course Tasks & Status")
        if not dept_assignments:
            st.info("No assignments published for your department yet.")
        else:
            for a in dept_assignments:
                # Find if current student submitted
                my_sub = next((s for s in a.get("submissions", []) if s.get("student_id") == student_id), None)
                
                status_badge = "🔴 Pending"
                grade_info = ""
                if my_sub:
                    if my_sub.get("status") == "Graded":
                        status_badge = f"🟢 Graded ({my_sub.get('grade')})"
                    else:
                        status_badge = "🟡 Submitted (Awaiting Grade)"
                        
                content = f"""
                <div style="margin-bottom: 5px;">
                    <p><b>Subject:</b> {a.get("subject")} | <b>Due Date:</b> <span style="color: #ef4444; font-weight:600;">{a.get("due_date")}</span></p>
                    <p><b>Description:</b> {a.get("description")}</p>
                    <p><b>My Status:</b> {status_badge}</p>
                </div>
                """
                st.markdown(card_wrapper(a.get("title"), content, "📋", theme), unsafe_allow_html=True)
                
    with tab_submit:
        st.markdown("### Upload Finished Coursework")
        
        # Select pending assignment
        unsubmitted_a = []
        for a in dept_assignments:
            has_submitted = any(s.get("student_id") == student_id for s in a.get("submissions", []))
            if not has_submitted:
                unsubmitted_a.append(a)
                
        if not unsubmitted_a:
            st.success("🎉 Excellent! You have submitted all published assignments.")
        else:
            select_sub_title = st.selectbox("Select Assignment", [a.get("title") for a in unsubmitted_a])
            target_sub_a = next((a for a in unsubmitted_a if a.get("title") == select_sub_title), None)
            
            if target_sub_a:
                with st.container(border=True):
                    st.markdown(f"**Description:** {target_sub_a.get('description')}")
                    
                    # File Uploader UI
                    uploaded_file = st.file_uploader("Upload Coursework File (PDF, ZIP, IPYNB)", type=["pdf", "zip", "ipynb"])
                    git_link = st.text_input("Or input Git Project Repository Link", placeholder="https://github.com/...")
                    
                    if st.button("Submit Assignment", use_container_width=True, type="primary"):
                        if not uploaded_file and not git_link:
                            st.error("Please upload a file or supply a Git project link.")
                        else:
                            # Append student submission object
                            new_submission = {
                                "student_id": student_id,
                                "student_name": st.session_state.name,
                                "submission_date": datetime.now().strftime("%Y-%m-%d"),
                                "status": "Submitted",
                                "grade": "Pending",
                                "file_url": git_link if git_link else (uploaded_file.name if uploaded_file else "#")
                            }
                            
                            submissions_list = target_sub_a.get("submissions", [])
                            submissions_list.append(new_submission)
                            
                            if update_json("assignments", target_sub_a.get("id"), {"submissions": submissions_list}):
                                # Also update student pending assignments counts
                                students_db = load_json("students")
                                student_profile = next((s for s in students_db if s.get("id") == st.session_state.user.get("id")), None)
                                if student_profile:
                                    # Increment completed and decrement pending
                                    new_comp = int(student_profile.get("completed_assignments", 0)) + 1
                                    new_pend = max(0, int(student_profile.get("pending_assignments", 0)) - 1)
                                    
                                    from utils.database import update_json as upd_s
                                    upd_s("students", student_profile.get("id"), {
                                        "completed_assignments": new_comp,
                                        "pending_assignments": new_pend
                                    })
                                    
                                st.success("Coursework successfully submitted! Your grades will be updated post lecturer review.")
                                st.rerun()
                            else:
                                st.error("Failed to register submission.")
