import streamlit as st
from utils.database import load_json, save_json
from utils.security import hash_password, verify_password, validate_email

def login_user(email: str, password: str) -> tuple[bool, str]:
    """Authenticate user and initialize session state."""
    users = load_json("users")
    user = next((u for u in users if u.get("email") == email), None)
    
    if not user:
        return False, "User account not found."
        
    if verify_password(password, user.get("password")):
        st.session_state.logged_in = True
        st.session_state.user = user
        st.session_state.role = user.get("role", "Student")
        st.session_state.email = user.get("email")
        st.session_state.name = user.get("name")
        return True, "Login successful."
        
    return False, "Incorrect password."

def register_user(name: str, email: str, password: str, mobile: str, department: str, student_id: str, role: str) -> tuple[bool, str]:
    """Register a new user and add profile details to database."""
    if not name or not email or not password or not department:
        return False, "Please fill in all required fields."
        
    if not validate_email(email):
        return False, "Invalid email address format."
        
    users = load_json("users")
    if any(u.get("email") == email for u in users):
        return False, "An account with this email already exists."
        
    if role == "Student" and not student_id:
        return False, "Student ID is required for student accounts."

    # Create user object
    user_id = f"u{len(users) + 1}"
    new_user = {
        "id": user_id,
        "name": name,
        "email": email,
        "password": hash_password(password),
        "department": department,
        "role": role,
        "student_id": student_id if role == "Student" else "",
        "mobile": mobile
    }
    
    users.append(new_user)
    if not save_json("users", users):
        return False, "Error saving user account data."
        
    # If Student, also create Student Profile
    if role == "Student":
        students = load_json("students")
        new_student = {
            "id": user_id,
            "name": name,
            "email": email,
            "department": department,
            "student_id": student_id,
            "cgpa": 0.0,
            "attendance_rate": 100.0,
            "joined_date": "",
            "completed_assignments": 0,
            "pending_assignments": 0,
            "books_borrowed": 0
        }
        students.append(new_student)
        save_json("students", students)
        
    return True, "Account registered successfully."

def logout_user():
    """Clear session state keys to sign user out."""
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.role = None
    st.session_state.email = None
    st.session_state.name = None
    # Force page rerun to clean UI
    st.rerun()
