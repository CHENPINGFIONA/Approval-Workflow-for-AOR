import streamlit as st
import os
import sqlite3
from pathlib import Path
from datetime import datetime

cwd = os.getcwd()
WORKING_DIRECTORY = os.path.join(cwd, "database")
if st.secrets["sql_ext_path"] == "None":
	WORKING_DATABASE= os.path.join(WORKING_DIRECTORY , st.secrets["default_db"])
else:
	WORKING_DATABASE= st.secrets["sql_ext_path"]


def prototype_application():
 
    # Set up the upload directory
    UPLOAD_DIRECTORY = os.path.join(cwd, "uploaded_files")
    if not os.path.exists(UPLOAD_DIRECTORY):
        os.makedirs(UPLOAD_DIRECTORY)

    st.title("Upload the AOR Template")
    
    # Category input
    category = st.text_input("Template Category:")

    # File uploader
    uploaded_files = st.file_uploader("Choose files", accept_multiple_files=True)

    if st.button("Upload"):
        if uploaded_files and category:
            for file in uploaded_files:
                file_path = os.path.join(UPLOAD_DIRECTORY, file.name)
                with open(file_path, "wb") as f:
                    f.write(file.getbuffer())
                st.success(f"File {file.name} has been uploaded successfully.")
        elif not category:
            st.warning("Please enter a category before uploading.")
        else:
            st.warning("Please select files to upload.")

    # Display uploaded files
    if uploaded_files:
        st.write("Uploaded files:")
        for file in uploaded_files:
            st.write(file.name)

    # Save button
    if st.button("Save to Database"):
        if uploaded_files and category:
            for file in uploaded_files:
                filename = file.name
                directory = os.path.abspath(UPLOAD_DIRECTORY)
                collect(filename,directory,category)
            st.success("Files information saved to database successfully.")
        elif not category:
            st.warning("Please enter a category before saving.")
        elif not uploaded_files:
            st.warning("Please upload files before saving.")

def collect(filename, directory, category):
	# collect data from template
	conn = sqlite3.connect(WORKING_DATABASE)
	cursor = conn.cursor()
	now = datetime.now()  # Using ISO format for date
	cursor.execute("INSERT INTO AOR_Template_Files VALUES (?, ?, ?,?)", (filename, directory, category, datetime.now()))
	conn.commit()
	conn.close()
 