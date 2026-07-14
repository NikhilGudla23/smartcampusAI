import json
import threading
from pathlib import Path
from datetime import datetime, timedelta
from utils.security import hash_password
import config

# Thread lock to prevent concurrent write issues in multi-user Streamlit environment
db_lock = threading.Lock()

def get_db_path(filename: str) -> Path:
    """Get the absolute path to a JSON database file."""
    if not filename.endswith(".json"):
        filename = f"{filename}.json"
    return config.DATABASE_DIR / filename

def load_json(filename: str) -> list:
    """Load list data from a JSON file. Returns empty list if not found."""
    path = get_db_path(filename)
    if not path.exists():
        return []
    
    with db_lock:
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []

def save_json(filename: str, data: list) -> bool:
    """Save list data to a JSON file."""
    path = get_db_path(filename)
    with db_lock:
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, default=str)
            return True
        except IOError:
            return False

def update_json(filename: str, item_id: str, new_data: dict, id_key: str = "id") -> bool:
    """Update a specific record in a JSON file list by its ID."""
    data = load_json(filename)
    updated = False
    
    for i, item in enumerate(data):
        if str(item.get(id_key)) == str(item_id):
            data[i].update(new_data)
            updated = True
            break
            
    if updated:
        return save_json(filename, data)
    return False

def delete_json(filename: str, item_id: str, id_key: str = "id") -> bool:
    """Delete a specific record in a JSON file list by its ID."""
    data = load_json(filename)
    filtered_data = [item for item in data if str(item.get(id_key)) != str(item_id)]
    
    if len(filtered_data) < len(data):
        return save_json(filename, filtered_data)
    return False

def seed_database():
    """Seed the database files with rich, beautiful mock data if they do not exist or are empty."""
    # Seed Users
    users_path = get_db_path("users")
    if not users_path.exists() or len(load_json("users")) == 0:
        seeded_users = [
            {
                "id": "u1",
                "name": "Nikhil Gupta",
                "email": "student@smartcampus.edu",
                "password": hash_password("Password123"),
                "department": "Computer Science",
                "role": "Student",
                "student_id": "CS-2024-042",
                "mobile": "+1234567890"
            },
            {
                "id": "u2",
                "name": "Emily Chen",
                "email": "emily@smartcampus.edu",
                "password": hash_password("Password123"),
                "department": "Electronics",
                "role": "Student",
                "student_id": "EC-2024-115",
                "mobile": "+1987654321"
            },
            {
                "id": "u3",
                "name": "Dr. Sarah Jenkins",
                "email": "faculty@smartcampus.edu",
                "password": hash_password("Password123"),
                "department": "Computer Science",
                "role": "Faculty",
                "mobile": "+1555123456"
            },
            {
                "id": "u4",
                "name": "Prof. David Miller",
                "email": "miller@smartcampus.edu",
                "password": hash_password("Password123"),
                "department": "Mathematics",
                "role": "Faculty",
                "mobile": "+1555654321"
            }
        ]
        save_json("users", seeded_users)

    # Seed Students profiles matching users
    students_path = get_db_path("students")
    if not students_path.exists() or len(load_json("students")) == 0:
        seeded_students = [
            {
                "id": "u1",
                "name": "Nikhil Gupta",
                "email": "student@smartcampus.edu",
                "department": "Computer Science",
                "student_id": "CS-2024-042",
                "cgpa": 3.85,
                "attendance_rate": 94.2,
                "joined_date": "2024-09-01",
                "completed_assignments": 18,
                "pending_assignments": 2,
                "books_borrowed": 3
            },
            {
                "id": "u2",
                "name": "Emily Chen",
                "email": "emily@smartcampus.edu",
                "department": "Electronics",
                "student_id": "EC-2024-115",
                "cgpa": 3.62,
                "attendance_rate": 88.5,
                "joined_date": "2024-09-01",
                "completed_assignments": 15,
                "pending_assignments": 5,
                "books_borrowed": 1
            }
        ]
        save_json("students", seeded_students)

    # Seed Attendance (historical log)
    attendance_path = get_db_path("attendance")
    if not attendance_path.exists() or len(load_json("attendance")) == 0:
        seeded_attendance = []
        subjects = {
            "Computer Science": ["Advanced AI", "Cloud Computing", "Algorithms"],
            "Electronics": ["Signal Processing", "Microcontrollers", "VLSI Design"],
            "Mathematics": ["Linear Algebra", "Calculus", "Probability"]
        }
        
        # Add past 10 days of attendance for student u1 and u2
        today = datetime.now()
        for i in range(12):
            date_str = (today - timedelta(days=i)).strftime("%Y-%m-%d")
            # Exclude weekends
            day_name = (today - timedelta(days=i)).strftime("%A")
            if day_name in ["Saturday", "Sunday"]:
                continue
                
            # Student 1 CS
            seeded_attendance.append({
                "id": f"att_u1_{i}",
                "student_id": "CS-2024-042",
                "student_name": "Nikhil Gupta",
                "department": "Computer Science",
                "date": date_str,
                "subject": "Advanced AI",
                "status": "Present" if i != 4 else "Absent",
                "marked_by": "faculty@smartcampus.edu"
            })
            seeded_attendance.append({
                "id": f"att_u1_c_{i}",
                "student_id": "CS-2024-042",
                "student_name": "Nikhil Gupta",
                "department": "Computer Science",
                "date": date_str,
                "subject": "Cloud Computing",
                "status": "Present",
                "marked_by": "faculty@smartcampus.edu"
            })
            
            # Student 2 EC
            seeded_attendance.append({
                "id": f"att_u2_{i}",
                "student_id": "EC-2024-115",
                "student_name": "Emily Chen",
                "department": "Electronics",
                "date": date_str,
                "subject": "Signal Processing",
                "status": "Present" if i % 6 != 0 else "Absent",
                "marked_by": "faculty@smartcampus.edu"
            })
        save_json("attendance", seeded_attendance)

    # Seed Timetable
    timetable_path = get_db_path("timetable")
    if not timetable_path.exists() or len(load_json("timetable")) == 0:
        seeded_timetable = [
            {"id": "t1", "department": "Computer Science", "day": "Monday", "subject": "Advanced AI", "time": "09:00 AM - 11:00 AM", "room": "Room 501", "faculty": "Dr. Sarah Jenkins"},
            {"id": "t2", "department": "Computer Science", "day": "Monday", "subject": "Cloud Computing", "time": "02:00 PM - 03:30 PM", "room": "Lab 4", "faculty": "Dr. Sarah Jenkins"},
            {"id": "t3", "department": "Computer Science", "day": "Tuesday", "subject": "Algorithms", "time": "10:00 AM - 12:00 PM", "room": "Room 503", "faculty": "Prof. David Miller"},
            {"id": "t4", "department": "Computer Science", "day": "Wednesday", "subject": "Advanced AI", "time": "09:00 AM - 11:00 AM", "room": "Room 501", "faculty": "Dr. Sarah Jenkins"},
            {"id": "t5", "department": "Computer Science", "day": "Thursday", "subject": "Cloud Computing", "time": "11:30 AM - 01:00 PM", "room": "Lab 4", "faculty": "Dr. Sarah Jenkins"},
            {"id": "t6", "department": "Electronics", "day": "Monday", "subject": "Signal Processing", "time": "10:00 AM - 12:00 PM", "room": "Room 201", "faculty": "Prof. David Miller"},
            {"id": "t7", "department": "Electronics", "day": "Tuesday", "subject": "Microcontrollers", "time": "09:00 AM - 11:00 AM", "room": "Lab 2", "faculty": "Dr. Sarah Jenkins"},
            {"id": "t8", "department": "Electronics", "day": "Thursday", "subject": "VLSI Design", "time": "01:30 PM - 03:30 PM", "room": "Room 204", "faculty": "Emily Chen (TA)"}
        ]
        save_json("timetable", seeded_timetable)

    # Seed Notifications
    notifications_path = get_db_path("notifications")
    if not notifications_path.exists() or len(load_json("notifications")) == 0:
        seeded_notifications = [
            {"id": "n1", "title": "End Semester Schedule Out", "message": "The final exams schedule for all engineering departments is now updated under files and timetable section. Exams start from next Monday.", "date": "2026-07-14 09:30", "type": "Exam", "recipient": "All"},
            {"id": "n2", "title": "AI Assistant Hackathon", "message": "Join the annual AI Hackathon. Registrations close on July 20th. Winner gets a smart home lab device!", "date": "2026-07-13 14:15", "type": "System", "recipient": "All"},
            {"id": "n3", "title": "New Assignment Posted: Advanced AI", "message": "Dr. Sarah Jenkins has posted Assignment 3: Transformers & NLP Models. Due date is July 22nd.", "date": "2026-07-12 11:00", "type": "Assignment", "recipient": "Student"},
            {"id": "n4", "title": "Library Book Overdue Warning", "message": "Friendly reminder to return 'Design Patterns in Python' to library counter to avoid overdue fine charges.", "date": "2026-07-11 08:00", "type": "System", "recipient": "student@smartcampus.edu"}
        ]
        save_json("notifications", seeded_notifications)

    # Seed Assignments
    assignments_path = get_db_path("assignments")
    if not assignments_path.exists() or len(load_json("assignments")) == 0:
        seeded_assignments = [
            {
                "id": "a1",
                "title": "Assignment 1: Neural Networks from Scratch",
                "description": "Implement backpropagation and gradient descent in pure NumPy for a 2-layer classifier.",
                "department": "Computer Science",
                "subject": "Advanced AI",
                "due_date": "2026-07-01",
                "created_by": "faculty@smartcampus.edu",
                "submissions": [
                    {"student_id": "CS-2024-042", "student_name": "Nikhil Gupta", "submission_date": "2026-06-30", "status": "Graded", "grade": "A", "file_url": "#"},
                    {"student_id": "EC-2024-115", "student_name": "Emily Chen", "submission_date": "2026-07-01", "status": "Graded", "grade": "B+", "file_url": "#"}
                ]
            },
            {
                "id": "a2",
                "title": "Assignment 2: Docker Containerization of Web Services",
                "description": "Deploy a multi-container flask app with postgres and redis caching using docker-compose.",
                "department": "Computer Science",
                "subject": "Cloud Computing",
                "due_date": "2026-07-10",
                "created_by": "faculty@smartcampus.edu",
                "submissions": [
                    {"student_id": "CS-2024-042", "student_name": "Nikhil Gupta", "submission_date": "2026-07-09", "status": "Graded", "grade": "A+", "file_url": "#"}
                ]
            },
            {
                "id": "a3",
                "title": "Assignment 3: Transformers & Fine-tuning LLMs",
                "description": "Fine-tune a distilbert model on text classification dataset and analyze accuracy metrics.",
                "department": "Computer Science",
                "subject": "Advanced AI",
                "due_date": "2026-07-25",
                "created_by": "faculty@smartcampus.edu",
                "submissions": []
            }
        ]
        save_json("assignments", seeded_assignments)

    # Seed Library Books
    library_path = get_db_path("library")
    if not library_path.exists() or len(load_json("library")) == 0:
        seeded_books = [
            {"id": "b1", "title": "Introduction to Algorithms", "author": "Thomas H. Cormen", "isbn": "978-0262033848", "category": "Computer Science", "status": "Available", "borrowed_by": None, "due_date": None},
            {"id": "b2", "title": "Deep Learning", "author": "Ian Goodfellow", "isbn": "978-0262035613", "category": "Computer Science", "status": "Borrowed", "borrowed_by": "student@smartcampus.edu", "due_date": "2026-07-28"},
            {"id": "b3", "title": "Design Patterns", "author": "Erich Gamma", "isbn": "978-0201633610", "category": "Software Engineering", "status": "Borrowed", "borrowed_by": "student@smartcampus.edu", "due_date": "2026-07-24"},
            {"id": "b4", "title": "Microelectronic Circuits", "author": "Adel S. Sedra", "isbn": "978-0199339136", "category": "Electronics", "status": "Available", "borrowed_by": None, "due_date": None},
            {"id": "b5", "title": "Calculus: Early Transcendentals", "author": "James Stewart", "isbn": "978-1285741550", "category": "Mathematics", "status": "Available", "borrowed_by": None, "due_date": None},
            {"id": "b6", "title": "Programming Rust", "author": "Jim Blandy", "isbn": "978-1492052593", "category": "Computer Science", "status": "Borrowed", "borrowed_by": "emily@smartcampus.edu", "due_date": "2026-07-30"}
        ]
        save_json("library", seeded_books)

# Run seed database automatically
seed_database()
