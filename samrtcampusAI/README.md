# SmartCampusAI ⚡

SmartCampusAI is a production-ready, modular, and AI-powered smart campus management platform built with Python, Streamlit, and a thread-safe JSON-based database. It features a responsive glassmorphic UI, rich Plotly analytics, role-based dashboards, and a virtual teaching assistant powered by Google Gemini.

---

## 🚀 Live Demo & Seed Accounts
For immediate testing, use the following pre-configured credentials:

| Role | Email | Password |
|---|---|---|
| **Student** | `student@smartcampus.edu` | `Password123` |
| **Faculty** | `faculty@smartcampus.edu` | `Password123` |

---

## ✨ Features
- **Aesthetic Glassmorphism UI**: Custom Tailwind/Vanilla CSS overlays, hover card shifts, and responsive dark/light transitions.
- **Dynamic Role Gating**: Role-specific dashboards (Student and Faculty portals) with permissioned visibility of directory controls, attendance marking, assignment creation, and grading desks.
- **Google Gemini Co-pilot**: High-fidelity academic assistant. Falls back to a local rules engine if no API key is specified, preventing service crashes.
- **Thread-safe CRUD operations**: Flat JSON databases with concurrent write thread locks, optimized for multi-user Streamlit processes.
- **Rich Interactive Analytics**: Live Plotly figures tracking attendance trends, department allocations, and assignment progress rates.

---

## 📁 Project Structure
```text
SmartCampusAI/
├── app.py                  # Main Entry Point & Landing Page
├── config.py               # Env/Path configurations
├── requirements.txt        # Package dependencies
├── .env                    # Secrets and API Keys
├── .gitignore              # Ignored files
├── README.md               # Documentation
│
├── assets/
│   ├── css/
│   │   └── style.css       # Core custom stylesheets
│   └── images/             # Static UI assets
│
├── database/               # Local JSON Database
│   ├── users.json
│   ├── students.json
│   ├── attendance.json
│   ├── timetable.json
│   ├── notifications.json
│   └── assignments.json
│
├── pages/                  # Streamlit Multi-page Routing
│   ├── Dashboard.py
│   ├── Login.py
│   ├── Register.py
│   ├── AI_Assistant.py
│   ├── Student.py
│   ├── Faculty.py
│   ├── Attendance.py
│   ├── Library.py
│   ├── Timetable.py
│   ├── Assignments.py
│   ├── Notifications.py
│   └── Settings.py
│
└── utils/                  # Backend Controller logic
    ├── auth.py             # Login & registration manager
    ├── database.py         # JSON locking database helper
    ├── helpers.py          # Card design & CSS wrappers
    ├── security.py         # SHA-256 Hashing helper
    └── ai.py               # Gemini interface & mock response fallback
```

---

## 🛠️ Local Installation & Setup

1. **Clone the repository** (or navigate to workspace):
   ```bash
   cd SmartCampusAI
   ```

2. **Create a virtual environment & activate it**:
   ```bash
   python -m venv venv
   # On Windows (PowerShell):
   .\venv\Scripts\Activate.ps1
   # On Linux/macOS:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup Environment Variables**:
   Copy the example environment settings to a local `.env` file:
   ```bash
   # Create a file named .env and paste:
   GEMINI_API_KEY=your_gemini_api_key_here
   SECRET_KEY=smartcampusai_secret_super_key_12345
   ```

5. **Run the application**:
   ```bash
   streamlit run app.py
   ```

---

## 🌐 Cloud Deployment Guide

This repository is optimized to deploy with zero compilation configurations.

### Streamlit Community Cloud
1. Push the code to a GitHub repository.
2. Visit [Streamlit Share](https://share.streamlit.io/) and click **New App**.
3. Choose the repository, branch, and set main file path to `app.py`.
4. Open **Advanced settings** and paste the environment variables under **Secrets**:
   ```toml
   GEMINI_API_KEY = "your_actual_gemini_key_here"
   SECRET_KEY = "your_secret_key"
   ```
5. Click **Deploy**.

### Render / Railway / HuggingFace Spaces
- Set build command to: `pip install -r requirements.txt`
- Set start command to: `streamlit run app.py --server.port 8080 --server.address 0.0.0.0`
- Define environment variables (`GEMINI_API_KEY`, `SECRET_KEY`) under the configuration dashboard panel.
