import streamlit as st
import os
import sqlite3
from pathlib import Path
from datetime import datetime
import pandas as pd

cwd = os.getcwd()
WORKING_DIRECTORY = os.path.join(cwd, "database")
if st.secrets["sql_ext_path"] == "None":
	WORKING_DATABASE= os.path.join(WORKING_DIRECTORY , st.secrets["default_db"])
else:
	WORKING_DATABASE= st.secrets["sql_ext_path"]


def prototype_application():
 
    st.title("AOR Approval")
    
    showAOR()
    remark = st.text_input("Remark:")

    
    if st.button("Approve"):
            st.success("AOR approved Successfully")
        
    if st.button("Return"):
            st.warning("AOR returned")   
        

    
def showAOR():
    # Connect to the specified database
    conn = sqlite3.connect(WORKING_DATABASE)
    cursor = conn.cursor()

    # Fetch all data from the AOR table
    cursor.execute("SELECT title, aor, submitted_by, submitted_on FROM AOR")
    rows = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]

    # Create a DataFrame from the fetched data
    df = pd.DataFrame(rows, columns=column_names)

    # Create hyperlinks for the "title" column
    df['title'] = df['title'].apply(lambda x: f'<a href="#" class="hyperlink">{x}</a>')

    # Display the table with hyperlinks using st.markdown
    st.markdown(df.to_html(escape=False, index=False), unsafe_allow_html=True)

    # Allow users to select a row (by index) using multiselect
    selected_row = st.multiselect("Select an AOR", df.index)

    # Display the corresponding AOR content based on the selected row
    if selected_row:
        selected_index = selected_row[0]  # Assume selecting one row at a time
        selected_aor = df.at[selected_index, "aor"]
        st.text_area("Selected AOR Content", selected_aor)

    # Close the connection
    conn.close()
    
