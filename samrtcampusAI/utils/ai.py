import os
import random
import google.generativeai as genai
import config

# Initialize Gemini Client if Key is Present
gemini_available = False
api_key = config.GEMINI_API_KEY or config.GOOGLE_API_KEY

if api_key and not api_key.startswith("your_"):
    try:
        genai.configure(api_key=api_key)
        # Verify model loading
        model = genai.GenerativeModel('gemini-1.5-flash')
        gemini_available = True
    except Exception as e:
        print(f"Error configuring Google Generative AI: {e}")

# Persona definitions
SYSTEM_INSTRUCTION = (
    "You are 'SmartCampusAI Copilot', an advanced virtual assistant embedded in the SmartCampusAI management platform. "
    "Your objective is to assist students and faculty members with campus-related inquiries, academic advice, scheduling queries, "
    "library search tips, assignment breakdowns, and software development concepts. "
    "Always maintain a polite, encouraging, and highly professional tone. "
    "Format your replies beautifully using clean Markdown, bold headers, and bullet points. Use code highlighting for source code."
)

def get_fallback_response(prompt: str) -> str:
    """Generate simulated responses based on keywords in prompt for fallback scenarios."""
    prompt_lower = prompt.lower()
    
    responses = {
        "hello": [
            "Hello! I am your SmartCampusAI Copilot. How can I help you navigate your academic journey today?",
            "Greetings! How may I assist you with your students record, library books, or timetables today?"
        ],
        "attendance": [
            "Under the SmartCampusAI system, attendance is updated in real-time by faculty. You can view your record under the 'Attendance' page. Remember, keeping attendance above **75%** is crucial for final exam eligibility.",
            "If you need to log attendance, please contact your department advisor or mark your presence directly on the Attendance dashboard during lecture hours."
        ],
        "assignment": [
            "Assignments are managed directly on the 'Assignments' section. Faculty can create tasks and grade submissions, while students can check details, download files, and upload completed documents. The upcoming assignment 'Transformers & Fine-tuning LLMs' is due on **July 25th**.",
            "To submit an assignment, go to the Assignments page, choose the active task from the list, click 'Submit' and fill out your details."
        ],
        "library": [
            "Our library catalog includes textbook listings for Computer Science, Electronics, and Mathematics. You can check availability under the 'Library' page. Active borrowings are marked with due dates; please return books on time to avoid fines.",
            "Need study materials? Search the catalog in the Library section to find the ISBN and reservation status of core text references."
        ],
        "timetable": [
            "Your weekly class schedules can be found in the 'Timetable' page. Filter classes by department and day to view lecture timings, rooms, and assigning faculty.",
            "Class hours are normally structured in slots starting from 09:00 AM to 04:00 PM. Check the timetable page for schedule shifts."
        ],
        "help": [
            "I can assist you with various campus queries! Try asking me about 'attendance rules', 'how to submit assignments', 'finding books in the library', or asking specific code questions!"
        ]
    }
    
    # Check keyword matches
    for key, val_list in responses.items():
        if key in prompt_lower:
            return random.choice(val_list)
            
    # Default fallback answer
    return (
        f"**[SIMULATED RESPONSE - API KEY NOT CONFIGURED]**\n\n"
        f"Thank you for asking: *\"{prompt}\"*.\n\n"
        f"To enable complete AI capability with Google Gemini, please configure a valid `GEMINI_API_KEY` in your `.env` file.\n\n"
        f"**Campus Core Info Details:**\n"
        f"- **Timetables & Class Schedules** are accessible in the sidebar.\n"
        f"- **Academic Minimum Requirement**: 75% attendance and timely assignment submissions.\n"
        f"- **Need Assistance?** Drop an inquiry to the student administration or type 'help' here."
    )

def generate_campus_response(prompt: str, chat_history: list = None) -> str:
    """Generate response using Gemini 1.5 Flash if available, otherwise fall back to local rule engine."""
    if gemini_available:
        try:
            # Build context from history
            contents = []
            if chat_history:
                # Add historical dialogue
                for msg in chat_history[-6:]:  # limit to last 3 exchanges (6 messages) to save tokens
                    role = "user" if msg["role"] == "user" else "model"
                    contents.append({"role": role, "parts": [msg["content"]]})
            
            # Format system instruction and append prompt
            full_prompt = f"{SYSTEM_INSTRUCTION}\n\nUser Question: {prompt}"
            
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            print(f"Gemini API run error: {e}")
            return f"*(Gemini encountered an error)*\n\n{get_fallback_response(prompt)}"
    else:
        return get_fallback_response(prompt)

def check_api_status() -> dict:
    """Return dictionary containing status details for various API integrations."""
    return {
        "Gemini API": "Connected & Available" if gemini_available else "Not Configured (Using Local Fallback Engine)",
        "OpenAI API": "Configured" if config.OPENAI_API_KEY else "Not Configured",
        "Database System": "Active (Local JSON Files)"
    }
