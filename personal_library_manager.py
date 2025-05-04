# import the required libraries
import os 
import json
import streamlit as st

# To define the library file
library_file = "library.txt"

# To load the library data from the file
def load_library():
    if os.path.exists(library_file):
        with open(library_file, "r") as f:
            return json.load(f)
           
    else:
        return []
    
# To save the library data to the file
def save_library(library):
    try:
        with open(library_file, "w") as f:
            json.dump(library, f, indent=4)
    except Exception as e:
        st.error(f"Error saving library: {e}")


# Initialize session state 
if "library" not in st.session_state:
     st.session_state.library = load_library()

# To set the title of the app
st.title("📚 Personal Library Manager")

# To set the menu bar"
menu = st.sidebar.radio("Menu",["Add Book", "Remove Book", "Search Book", "Display All Books", "Statistics", "Save & Exit"])

# To add a book in the library
if menu == "Add Book":
    st.subheader("➕ Add a New Book")

    with st.form("Add Book", clear_on_submit=True):
        title = st.text_input("Title")
        author = st.text_input("Author Name").title()
        year = st.number_input("Year of Publication", min_value=0, max_value=2025, value=2025, step=1)
        genre = st.text_input("Genre").title()
        read = st.selectbox("Did you read it ?", ["Yes","No"])
        rating = st.selectbox("Rating", ["1", "2", "3", "4", "5"])
        submitted = st.form_submit_button("Save Book")

        if submitted:
            if title and author and year and genre:
                new_book = {
                    "title": title,
                     "author": author,
                     "year": year,
                     "genre": genre,
                     "read": read,
                     "rating": rating
                }
                st.session_state.library.append(new_book)
                save_library(st.session_state.library)

                st.success(f"Book '{title}' by {author} added successfully")

# To remove a book from the library
if menu == "Remove Book":
    st.subheader("🗑️ Remove a Book")

    if len(st.session_state.library) == 0:
        st.warning("No books in the library yet")
    else:
        book_title = [book["title"] for book in st.session_state.library]
        if book_title:
          select_book_for_remove = st.selectbox("Select book to remove", book_title)

        if st.button("Remove Book"):
             st.session_state.library = [b for b in st.session_state.library if b["title"] != select_book_for_remove]
             save_library(st.session_state.library)
             st.success(f"Book '{select_book_for_remove}' removed successfully")

# To search a book in the library
if menu == "Search Book":
    st.subheader("🔍 Search for a Book")

    search_by = st.radio("Search by" , ["Title" , "Author"])
    query = st.text_input(f"Enter {search_by} name for search")

    if query:
        result = [b for b in st.session_state.library if query.lower() in b[search_by.lower()].lower() ]

        if result:
            for book in result:
                st.markdown(f"**{book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {'✅ Read' if book['read'] else '❌ Unread'}")
        else:
            st.warning("No matching book found")

# To display all books in the library
if menu == "Display All Books":
    st.subheader("📖 All Books in the Library")

    if len(st.session_state.library) == 0:
        st.info("Library is empty")
    else:
        for idx, book in enumerate(st.session_state.library, start=1):
            st.markdown(f"**{idx}. {book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {'✅ Read' if book['read'] else '❌ Unread'}")

# To display statistics
if menu == "Statistics":
    st.subheader("📊 Library Statistics")
    
    total_books = len(st.session_state.library)
    read_books = sum(1 for book in st.session_state.library if book['read'])
    unread_books = total_books - read_books

    st.write(f"Total books : **{total_books}**")
    st.write(f"Read books : **{read_books}**")
    st.write(f"Unread books : **{unread_books}**")

    # To display the percentage of read and unread books
    if total_books > 0:
        read_percentage = round((read_books / total_books) * 100, 2)
        unread_percentage = round((unread_books / total_books) * 100 ,2)

        st.write(f"Read percentage : **{read_percentage}%**")
        st.write(f"Unread percentage : **{unread_percentage}%**")

# To save and exit the app
if menu == "Save & Exit":
    save_library(st.session_state.library)
    st.success("Library saved successfully")
    st.stop()
