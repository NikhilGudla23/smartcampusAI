import streamlit as st
from utils.ai import generate_campus_response, check_api_status
from utils.helpers import inject_custom_css

# Gating
if not st.session_state.get("logged_in", False):
    st.warning("Please sign in to access this page.")
    st.switch_page("pages/Login.py")
    st.stop()

# Styling
inject_custom_css()
theme = st.session_state.theme

st.markdown("<h1>Gemini AI Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #94a3b8;'>Ask questions about course files, programming code, student workloads, or library reserves.</p>", unsafe_allow_html=True)

# Initialize Chat Messages in Session State
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {"role": "assistant", "content": "Hello! I am your SmartCampusAI Copilot. How can I assist you with your academic work, lecture timings, or coursework today?"}
    ]

# Sidebar Chat Controls
st.sidebar.subheader("AI Assistant Options")

# Show Connection Status
status_dict = check_api_status()
gemini_status = status_dict.get("Gemini API", "")
status_color = "🔴"
if "Available" in gemini_status:
    status_color = "🟢"
elif "Fallback" in gemini_status:
    status_color = "🟡"

st.sidebar.markdown(f"**Gemini Model Engine:** {status_color} {gemini_status}")

# Clear Chat Button
if st.sidebar.button("🧹 Clear Chat History", use_container_width=True, type="secondary"):
    st.session_state.chat_messages = [
        {"role": "assistant", "content": "Hello! Chat cleared. How can I assist you with your academic work today?"}
    ]
    st.toast("Chat history cleared!", icon="🧹")
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("""
**Suggested Prompts to try:**
- *\"What assignments are due for Computer Science?\"*
- *\"How can I improve my CGPA?\"*
- *\"What is the attendance policy?\"*
- *\"Explain how transformers work in AI.\"*
""")

# Render Chat History
for msg in st.session_state.chat_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User prompt input
prompt = st.chat_input("Ask your SmartCampusAI Copilot...")
if prompt:
    # Render user prompt
    with st.chat_message("user"):
        st.markdown(prompt)
        
    # Append to state
    st.session_state.chat_messages.append({"role": "user", "content": prompt})
    
    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing queries and drafting response..."):
            response = generate_campus_response(prompt, st.session_state.chat_messages)
            st.markdown(response)
            
    # Append to state
    st.session_state.chat_messages.append({"role": "assistant", "content": response})
    st.rerun()
