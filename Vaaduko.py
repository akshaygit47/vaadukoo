import streamlit as st
import os
import json

# Directory for storing notes
NOTES_DIR = "notes"
PASSWORD = "2035"

# Ensure notes directory exists
if not os.path.exists(NOTES_DIR):
    os.makedirs(NOTES_DIR)

# Load notes from the notes directory
def load_notes():
    notes = {}
    for filename in os.listdir(NOTES_DIR):
        if filename.endswith('.json'):
            with open(os.path.join(NOTES_DIR, filename), 'r') as f:
                note_data = json.load(f)
                notes[note_data['title']] = note_data
    return notes

# Save a note to the notes directory
def save_note_to_file(title, content):
    note_data = {
        'title': title,
        'note': content
    }
    with open(os.path.join(NOTES_DIR, f"{title}.json"), 'w') as f:
        json.dump(note_data, f)

# Delete a note from the notes directory
def delete_note_from_file(title):
    note_file = os.path.join(NOTES_DIR, f"{title}.json")
    if os.path.exists(note_file):
        os.remove(note_file)

# Password Screen
def password_screen():
    st.title("Diary App")
    st.write("Enter the password to continue")
    password_input = st.text_input("Password", type="password")

    if st.button("Submit"):
        if password_input == PASSWORD:
            st.session_state['page'] = 'home'
        else:
            st.error("Incorrect Password!")

# Home Screen
def home_screen():
    st.title("Diary App - Home")
    st.text_input("Search", placeholder="Search notes...")

    # List of saved notes
    notes = load_notes()

    st.subheader("Saved Notes")
    for title, content in notes.items():
        if st.button(title):
            st.session_state['note_title'] = title
            st.session_state['note_content'] = content
            st.session_state['page'] = 'note'

    if st.button("+ Add Note", key="add_note"):
        st.session_state['note_title'] = ""
        st.session_state['note_content'] = {}
        st.session_state['page'] = 'note'

# Note Screen
def note_screen():
    st.title("New Note" if not st.session_state['note_title'] else st.session_state['note_title'])

    # Ensure session_state['note_content'] is a dictionary
    if not isinstance(st.session_state.get('note_content'), dict):
        st.session_state['note_content'] = {}

    title = st.text_input("Title", value=st.session_state.get('note_title', ''))
    content = st.text_area("Note", value=st.session_state['note_content'].get('note', ''))

    if st.button("Save"):
        if title:
            save_note_to_file(title, content)
            st.session_state['page'] = 'home'
        else:
            st.error("Title cannot be empty!")

    if st.button("Delete"):
        delete_note_from_file(title)
        st.session_state['page'] = 'home'

    if st.button("Back"):
        st.session_state['page'] = 'home'

# Main App Logic
def main():
    if 'page' not in st.session_state:
        st.session_state['page'] = 'password'
    
    if st.session_state['page'] == 'password':
        password_screen()
    elif st.session_state['page'] == 'home':
        home_screen()
    elif st.session_state['page'] == 'note':
        note_screen()

if __name__ == "__main__":
    main()
