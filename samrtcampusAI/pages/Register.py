import streamlit as st
import time
from utils.auth import register_user
from utils.security import validate_password_strength
from utils.helpers import inject_custom_css

# Style
inject_custom_css()

col_left, col_mid, col_right = st.columns([1, 2, 1])

with col_mid:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center;">
        <span style="font-size: 3rem;">📝</span>
        <h1 style="margin: 10px 0 5px 0;">Create Account</h1>
        <p style="color: #94a3b8; margin-bottom: 20px;">Join the SmartCampusAI management system</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container(border=True):
        role = st.selectbox("I am registering as a", ["Student", "Faculty"])
        
        name = st.text_input("Full Name", placeholder="e.g. Nikhil Gupta")
        email = st.text_input("Email Address", placeholder="e.g. nikhil@smartcampus.edu")
        mobile = st.text_input("Mobile Number", placeholder="e.g. +1234567890")
        
        departments = ["Computer Science", "Electronics", "Mathematics", "Mechanical Engineering", "Business Admin"]
        department = st.selectbox("Department / Division", departments)
        
        # Student ID field only active/required for students
        student_id = ""
        if role == "Student":
            student_id = st.text_input("Student ID", placeholder="e.g. CS-2024-042")
            
        pass1 = st.text_input("Password", type="password", placeholder="••••••••")
        pass2 = st.text_input("Confirm Password", type="password", placeholder="••••••••")
        
        terms = st.checkbox("I agree to the Terms of Service & Privacy Policy")
        
        st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
        
        if st.button("Register Account", use_container_width=True, type="primary"):
            if not terms:
                st.error("You must accept the Terms of Service to register.")
            elif pass1 != pass2:
                st.error("Passwords do not match.")
            else:
                # Password strength check
                is_strong, pass_msg = validate_password_strength(pass1)
                if not is_strong:
                    st.error(pass_msg)
                else:
                    with st.spinner("Creating profile security records..."):
                        success, message = register_user(
                            name=name,
                            email=email,
                            password=pass1,
                            mobile=mobile,
                            department=department,
                            student_id=student_id,
                            role=role
                        )
                        if success:
                            st.success("Registration Successful! Redirecting to Sign In...")
                            time.sleep(1.5)
                            st.switch_page("pages/Login.py")
                        else:
                            st.error(message)
                            
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align: center; color: #94a3b8;'>"
        "Already have an account? "
        "<a href='/Login' target='_self' style='color: #6366f1; text-decoration: none; font-weight: 600;'>Sign In</a>"
        "</p>", 
        unsafe_allow_html=True
    )
    
    # If standard link fails, provide button
    if st.button("🔑 Sign In Page Redirect", use_container_width=True):
        st.switch_page("pages/Login.py")
        
    if st.button("🏠 Return Home", use_container_width=True):
        st.switch_page("app.py")
