# Import required libraries
import os
import json
import streamlit as st

# Define the library file
library_file = "library.txt"

# Load the library data from the file
def load_library():
    if os.path.exists(library_file):
        with open(library_file, "r") as f:
            return json.load(f)
    else:
        return []

# Save the library data to the file
def save_library(library):
    try:
        with open(library_file, "w") as f:
            json.dump(library, f, indent=4)
    except Exception as e:
        st.error(f"Error saving library: {e}")

# Initialize session state
if "library" not in st.session_state:
    st.session_state.library = load_library()

# Set the title of the app
st.title("📚 Personal Library Manager")

# Set the menu bar
menu = st.sidebar.radio("Menu", ["Add Book", "Remove Book", "Search Book", "Display All Books", "Statistics", "Save & Exit"])

# Add a book to the library
if menu == "Add Book":
    st.subheader("➕ Add a New Book")
    with st.form("Add Book", clear_on_submit=True):
        title = st.text_input("Title")
        author = st.text_input("Author Name").title()
        year = st.number_input("Year of Publication", min_value=0, max_value=2025, value=2025, step=1)
        genre = st.text_input("Genre").title()
        read = st.selectbox("Did you read it?", ["Yes", "No"])
        rating = st.selectbox("Rating", ["1", "2", "3", "4", "5"])
        submitted = st.form_submit_button("Save Book")

        if submitted:
            if title and author and genre:
                new_book = {
                    "title": title,
                    "author": author,
                    "year": year,
                    "genre": genre,
                    "read": read == "Yes",  # Store as boolean
                    "rating": rating
                }
                st.session_state.library.append(new_book)
                save_library(st.session_state.library)
                st.success(f"Book '{title}' by {author} added successfully!")

# Remove a book from the library
elif menu == "Remove Book":
    st.subheader("🗑️ Remove a Book")
    if not st.session_state.library:
        st.warning("No books in the library yet.")
    else:
        book_titles = [book["title"] for book in st.session_state.library]
        selected_book = st.selectbox("Select a book to remove", book_titles)
        if st.button("Remove Book"):
            st.session_state.library = [b for b in st.session_state.library if b["title"] != selected_book]
            save_library(st.session_state.library)
            st.success(f"Book '{selected_book}' removed successfully.")

# Search for a book
elif menu == "Search Book":
    st.subheader("🔍 Search for a Book")
    search_by = st.radio("Search by", ["Title", "Author"])
    query = st.text_input(f"Enter {search_by} name to search")

    if query:
        results = [
            b for b in st.session_state.library
            if query.lower() in b[search_by.lower()].lower()
        ]
        if results:
            for book in results:
                st.markdown(f"**{book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - "
                            f"{'✅ Read' if book['read'] else '❌ Unread'} - ⭐ {book['rating']}/5")
        else:
            st.warning("No matching books found.")

# Display all books
elif menu == "Display All Books":
    st.subheader("📖 Display All Books")
    if not st.session_state.library:
        st.info("Library is empty.")
    else:
        for idx, book in enumerate(sorted(st.session_state.library, key=lambda x: x["title"]), start=1):
            st.markdown(f"**{idx}. {book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - "
                        f"{'✅ Read' if book['read'] else '❌ Unread'} - ⭐ {book['rating']}/5")

# Library statistics
elif menu == "Statistics":
    st.subheader("📊 Library Statistics")
    total_books = len(st.session_state.library)
    if total_books == 0:
        st.info("No books in the library.")
    else:
        read_books = sum(1 for book in st.session_state.library if book["read"])
        unread_books = total_books - read_books
        read_percent = round((read_books / total_books) * 100, 2)
        unread_percent = round((unread_books / total_books) * 100, 2)

        st.write(f"**Total Books:** {total_books}")
        st.write(f"**Books Read:** {read_books}")
        st.write(f"**Books Unread:** {unread_books}")
        st.write(f"**Read Percentage:** {read_percent}%")
        st.write(f"**Unread Percentage:** {unread_percent}%")

# Save & exit
elif menu == "Save & Exit":
    save_library(st.session_state.library)
    st.success("Library saved successfully. Exiting...")
    st.stop()
