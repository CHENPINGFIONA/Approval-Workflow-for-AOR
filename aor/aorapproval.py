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
	# collect data from template
	# Connect to the specified database
	conn = sqlite3.connect(WORKING_DATABASE)
	cursor = conn.cursor()

	# Fetch all data from data_table
	cursor.execute("SELECT title, aor, submitted_by, submitted_on FROM AOR")
	rows = cursor.fetchall()
	column_names = [description[0] for description in cursor.description]
	df = pd.DataFrame(rows, columns=column_names)
	st.dataframe(df)
	conn.close()
