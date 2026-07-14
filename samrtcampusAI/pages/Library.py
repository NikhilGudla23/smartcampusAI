import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
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

st.markdown("<h1>Library Center</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #94a3b8;'>Search for textbooks, reserve research publications, and track borrowing logs.</p>", unsafe_allow_html=True)

role = st.session_state.role
books = load_json("library")

# Sidebar Search
st.sidebar.subheader("Library Search")
search_title = st.sidebar.text_input("Search Title / Author", "").strip().lower()
search_cat = st.sidebar.selectbox("Filter Category", ["All", "Computer Science", "Electronics", "Software Engineering", "Mathematics"])

# Apply filters
filtered_books = books
if search_title:
    filtered_books = [
        b for b in filtered_books
        if search_title in b.get("title", "").lower() or search_title in b.get("author", "").lower()
    ]
if search_cat != "All":
    filtered_books = [b for b in filtered_books if b.get("category") == search_cat]

# Render Tabs
if role == "Faculty":
    tab_catalog, tab_logs, tab_add = st.tabs(["📚 Book Catalog", "📋 Borrowing Logs", "➕ Add Catalog Book"])
else:
    tab_catalog, tab_my = st.tabs(["📚 Book Catalog", "🎒 My Borrowings"])

# 1. CATALOG TAB
with tab_catalog:
    st.markdown("### Catalog Textbooks")
    if not filtered_books:
        st.info("No books match the filters.")
    else:
        df_books = pd.DataFrame(filtered_books)
        df_show = df_books[["id", "title", "author", "isbn", "category", "status", "due_date"]].copy()
        df_show.columns = ["Book ID", "Title", "Author", "ISBN", "Category", "Status", "Due Date"]
        st.dataframe(df_show, use_container_width=True, hide_index=True)
        
        # Student Borrowing Action
        if role == "Student":
            st.markdown("---")
            st.markdown("### Borrow / Return Actions")
            
            # Select book to borrow or return
            selected_book_id = st.selectbox("Select Book ID to Action", [b.get("id") for b in filtered_books])
            target_book = next((b for b in books if b.get("id") == selected_book_id), None)
            
            if target_book:
                student_email = st.session_state.email
                
                # Check status
                if target_book.get("status") == "Available":
                    if st.button("📖 Borrow Selected Book", use_container_width=True, type="primary"):
                        due_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
                        update_data = {
                            "status": "Borrowed",
                            "borrowed_by": student_email,
                            "due_date": due_date
                        }
                        
                        if update_json("library", target_book.get("id"), update_data):
                            # Also update student borrow count in student table
                            students_db = load_json("students")
                            student_profile = next((s for s in students_db if s.get("email") == student_email), None)
                            if student_profile:
                                from utils.database import update_json as upd_s
                                new_count = int(student_profile.get("books_borrowed", 0)) + 1
                                upd_s("students", student_profile.get("id"), {"books_borrowed": new_count})
                                
                            st.success(f"Successfully borrowed '{target_book.get('title')}'! Return due date: {due_date}.")
                            st.rerun()
                        else:
                            st.error("Failed to process transaction.")
                else:
                    # Book is Borrowed. Is it borrowed by the current student?
                    if target_book.get("borrowed_by") == student_email:
                        if st.button("↩️ Return Selected Book", use_container_width=True, type="secondary"):
                            update_data = {
                                "status": "Available",
                                "borrowed_by": None,
                                "due_date": None
                            }
                            
                            if update_json("library", target_book.get("id"), update_data):
                                # Also update student borrow count in student table
                                students_db = load_json("students")
                                student_profile = next((s for s in students_db if s.get("email") == student_email), None)
                                if student_profile:
                                    from utils.database import update_json as upd_s
                                    new_count = max(0, int(student_profile.get("books_borrowed", 0)) - 1)
                                    upd_s("students", student_profile.get("id"), {"books_borrowed": new_count})
                                    
                                st.success(f"Thank you for returning '{target_book.get('title')}'!")
                                st.rerun()
                            else:
                                st.error("Failed to process return transaction.")
                    else:
                        st.warning(f"This book is currently checked out by another student. Due back on: {target_book.get('due_date')}")

# 2. BORROWINGS / MY TAB
if role == "Faculty":
    with tab_logs:
        st.markdown("### Outstanding Campus Borrowings")
        borrowed = [b for b in books if b.get("status") == "Borrowed"]
        if not borrowed:
            st.info("No books are currently checked out.")
        else:
            df_borrowed = pd.DataFrame(borrowed)
            st.dataframe(
                df_borrowed[["id", "title", "category", "borrowed_by", "due_date"]],
                use_container_width=True,
                hide_index=True
            )
            
    with tab_add:
        st.markdown("### Add Book to Catalog")
        with st.container(border=True):
            add_title = st.text_input("Book Title", placeholder="e.g. Introduction to Machine Learning")
            add_author = st.text_input("Author Name", placeholder="e.g. Ethem Alpaydin")
            add_isbn = st.text_input("ISBN", placeholder="e.g. 978-0262012430")
            add_category = st.selectbox("Category", ["Computer Science", "Electronics", "Software Engineering", "Mathematics"])
            
            if st.button("Add Textbook", use_container_width=True, type="primary"):
                if not add_title or not add_author or not add_isbn:
                    st.error("Please fill out all details.")
                else:
                    new_book = {
                        "id": f"b{len(books) + 1}",
                        "title": add_title,
                        "author": add_author,
                        "isbn": add_isbn,
                        "category": add_category,
                        "status": "Available",
                        "borrowed_by": None,
                        "due_date": None
                    }
                    
                    books.append(new_book)
                    if save_json("library", books):
                        st.success(f"Book '{add_title}' added to directory.")
                        st.rerun()
                    else:
                        st.error("Failed to add book.")
else:
    with tab_my:
        st.markdown("### My Borrowed Textbooks")
        my_borrowed = [b for b in books if b.get("borrowed_by") == st.session_state.email]
        if not my_borrowed:
            st.info("You do not have any active borrowings.")
        else:
            df_my = pd.DataFrame(my_borrowed)
            df_my_show = df_my[["title", "author", "isbn", "due_date"]].copy()
            df_my_show.columns = ["Title", "Author", "ISBN", "Due Return Date"]
            st.dataframe(df_my_show, use_container_width=True, hide_index=True)
