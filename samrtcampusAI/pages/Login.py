import streamlit as st
from utils.auth import login_user
from utils.helpers import inject_custom_css

# Ensure styling
inject_custom_css()

# Center Layout
col_left, col_mid, col_right = st.columns([1, 2, 1])

with col_mid:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center;">
        <span style="font-size: 3rem;">🔒</span>
        <h1 style="margin: 10px 0 5px 0;">Sign In Portal</h1>
        <p style="color: #94a3b8; margin-bottom: 30px;">Access your SmartCampusAI academic dashboard</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Glassmorphism Card simulated by Streamlit Container
    with st.container(border=True):
        email = st.text_input("Email Address", placeholder="e.g. student@smartcampus.edu")
        
        # Password Visibility Toggle
        show_password = st.checkbox("Show Password")
        password = st.text_input(
            "Password", 
            type="default" if show_password else "password",
            placeholder="••••••••"
        )
        
        # Remember and Forgot Password
        col_rem, col_forgot = st.columns([1, 1])
        with col_rem:
            st.checkbox("Remember Me", value=True)
        with col_forgot:
            st.markdown(
                "<div style='text-align: right; margin-top: 4px;'>"
                "<a href='#' style='color: #6366f1; text-decoration: none; font-size: 0.9rem;'>Forgot Password?</a>"
                "</div>", 
                unsafe_allow_html=True
            )
            
        st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
        
        # Action button
        if st.button("Login", use_container_width=True, type="primary"):
            if not email or not password:
                st.error("Please fill in both email and password fields.")
            else:
                with st.spinner("Authenticating secure credentials..."):
                    success, message = login_user(email, password)
                    if success:
                        st.success("Login Successful! Preparing dashboard...")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error(message)
                        
        st.markdown("<hr style='border-color: rgba(255,255,255,0.05); margin: 20px 0;'>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 0.85rem;'>Or login with</p>", unsafe_allow_html=True)
        
        # Social logins (UI only)
        social_1, social_2 = st.columns(2)
        with social_1:
            if st.button("🌐 Google Login", use_container_width=True):
                st.toast("Google Auth is under maintenance. Please use standard email login.", icon="⚙️")
        with social_2:
            if st.button("🐙 GitHub Login", use_container_width=True):
                st.toast("GitHub Auth is under maintenance. Please use standard email login.", icon="⚙️")
                
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align: center; color: #94a3b8;'>"
        "Don't have an account? "
        "<a href='/Register' target='_self' style='color: #6366f1; text-decoration: none; font-weight: 600;'>Create Account</a>"
        "</p>", 
        unsafe_allow_html=True
    )
    
    # If standard href navigation fails in Streamlit sandbox, use this standard button
    if st.button("📝 Register Page Redirect", use_container_width=True):
        st.switch_page("pages/Register.py")
        
    if st.button("🏠 Return Home", use_container_width=True):
        st.switch_page("app.py")
