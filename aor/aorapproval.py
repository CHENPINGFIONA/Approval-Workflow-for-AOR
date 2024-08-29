import streamlit as st
import os
import sqlite3
from pathlib import Path
from datetime import datetime
import pandas as pd
import streamlit.components.v1 as components

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

    
    if st.button("Approve", type="primary"):
            st.success("AOR approved Successfully")
        
    if st.button("Return", type="secondary"):
            st.warning("AOR returned")   
        

    
def showAOR():
    # Connect to the specified database
    conn = sqlite3.connect(WORKING_DATABASE)
    cursor = conn.cursor()

    # Fetch all data from the AOR table
    cursor.execute("SELECT title, submitted_by, submitted_on FROM AOR")
    rows = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]


    # Create a DataFrame from the fetched data
    df = pd.DataFrame(rows, columns=column_names)

    # Display the table with hyperlinks using st.markdown
    st.markdown(df.to_html(escape=False, index=False), unsafe_allow_html=True)

    df2=generate_selectlist()
    
    # Create a list of titles to display in the selectbox
    titles = df2['title'].tolist()

    # Use st.selectbox for single selection
    selected_title = st.selectbox("Select an AOR", titles)

    # Find the row corresponding to the selected title and display the AOR content
    if selected_title:
        selected_aor = df2.loc[df['title'] == selected_title, 'aor'].values[0]
        st.divider()
        st.write(selected_aor)
    # Close the connection
    conn.close()
    

def generate_selectlist():
    conn = sqlite3.connect(WORKING_DATABASE)
    cursor = conn.cursor()
    
    # Fetch all data from the AOR table
    cursor.execute("SELECT title, aor FROM AOR")
    rows = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    
    
    # Close the connection
    conn.close()
    
    return pd.DataFrame(rows, columns=column_names)