import streamlit as st
import os
import sqlite3
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
    
    # template name input
    template_name = st.text_input("AOR Template Name:")

    # File uploader
    uploaded_file = st.file_uploader("Upload a file")

    if st.button("Upload"):
        file_path = os.path.join(UPLOAD_DIRECTORY, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
            save_to_db(file_path,template_name)
            st.success(f"File {uploaded_file.name} has been uploaded successfully.")
    elif not template_name:
        st.warning("Please enter a template name before uploading.")
    else:
        st.warning("Please select file to upload.")
        

    

def save_to_db( directory, template_name):
	# collect data from template
	conn = sqlite3.connect(WORKING_DATABASE)
	cursor = conn.cursor()
	cursor.execute("INSERT INTO AOR_Template_Files (name,directory,uploaded_by,uploaded_on) VALUES (?, ?,?,?)", ( directory, template_name, st.session_state.user["username"],datetime.now()))
	conn.commit()
	conn.close()
 
