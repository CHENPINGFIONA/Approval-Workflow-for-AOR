import streamlit as st
import os
from fpdf import FPDF
import openai
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory
from langchain.chat_models import ChatOpenAI
from langchain.agents import ConversationalChatAgent, AgentExecutor
from langchain.callbacks import StreamlitCallbackHandler
from basecode.authenticate import (
    return_api_key,
    return_base_url
)

import sqlite3
from datetime import datetime

client = openai.OpenAI(
    api_key=return_api_key(),
    base_url=return_base_url(),
	)

cwd = os.getcwd()
WORKING_DIRECTORY = os.path.join(cwd, "database")
if st.secrets["sql_ext_path"] == "None":
	WORKING_DATABASE= os.path.join(WORKING_DIRECTORY , st.secrets["default_db"])
else:
	WORKING_DATABASE= st.secrets["sql_ext_path"]


def generate_aor(selected_path):   
    # This is a placeholder function. Replace with your actual text generation logic
    
    with open(selected_path,"r", encoding='utf-8',errors='ignore') as file:
        file_contents=file.read()
    response = client.chat.completions.create(
    	model="gpt-4o-mini",  
    	messages=[
			{
			"role": "user",
            "content": "Please generate AOR with minimum 1000 characters based on the template given here \n "+file_contents,
			}
    	])
	
    return response.choices[0].message.content


# Main application function
def prototype_application():
    st.title("AOR Generator")

    # Get the templates (you can modify `get_templates()` to fetch actual data)
    templates = get_templates()

    # Check if the list is empty
    if not templates:
        st.warning("Please upload a template.")
    else:
        renderUI(templates)
 
 
def renderUI(templates):
    name_to_path={template[2]:template[1] for template in templates}
    
    selected_name=st.selectbox("Select a Template:",list(name_to_path.keys()))
    selected_path=name_to_path[selected_name]
 
	# Generate button
    if st.button("Generate", type="primary"):
        generated_aor = generate_aor(selected_path)
        st.session_state.text_area_value = generated_aor

    title = st.text_input("AOR Title:")
	# Text area
    text_area = st.text_area("Generated Text:", value=st.session_state.get('text_area_value', ''), height=500)

  
	# Submit button
    if st.button("Submit",disabled=not title,type="primary"):
        save_aor_to_db(title, text_area)
        st.success(f"AOR {title} has been saved successfully.")
		
    
    # Save as template  button
    if st.button("Save as Template",disabled=not title,type="secondary"):
        file_path=save_to_file(title,text_area)
        save_template_to_db(file_path,title)
        st.success(f"Template {title} has been saved successfully.")
     
    aor_chatbot(text_area)
       
def aor_chatbot(generated_aor):

	# Initialize chat history
	if "messages" not in st.session_state:
		st.session_state.messages = []

	# Display chat messages from history on app rerun
	for message in st.session_state.messages:
		with st.chat_message(message["role"]):
			st.markdown(message["content"])
	
	# React to user input
	if prompt := st.chat_input("Enter your instruction here"):
		
		
		# Display user message in chat message container
		st.chat_message("user").markdown(prompt)
		# Add user message to chat history
		st.session_state.messages.append({"role": "user", "content": prompt})
		
  		#modify the code below to create an AI chatbot ( challenge 3)
		response = chat_completion("You are a helpful assistant", generated_aor+"\n"+prompt)

		# Display assistant response in chat message container
		with st.chat_message("assistant"):
			st.session_state.text_area_value = response
		# Add assistant response to chat history
		st.session_state.messages.append({"role": "assistant", "content": response})
		st.rerun()

def chat_completion(prompt_design, prompt):
	MODEL = "gpt-4o-mini"
	response = client.chat.completions.create(
		model=MODEL,
		messages=[
			{"role": "system", "content": prompt_design},
			{"role": "user", "content": prompt},
		],
		temperature=0,
	)
	return response.choices[0].message.content.strip()
  

def save_aor_to_db(title,generated_aor):
	# collect data from template
	conn = sqlite3.connect(WORKING_DATABASE)
	cursor = conn.cursor()
	now = datetime.now()  # Using ISO format for date
	cursor.execute("INSERT INTO AOR (title,aor,submitted_by,submitted_on) VALUES (?, ?, ?,?)", (title, generated_aor, st.session_state.user["username"], datetime.now()))
	conn.commit()
	conn.close()
 
 
def save_template_to_db(directory, template_name):
	# collect data from template
	conn = sqlite3.connect(WORKING_DATABASE)
	cursor = conn.cursor()
	cursor.execute("INSERT INTO AOR_Template_Files (name,directory,uploaded_by,uploaded_on) VALUES (?, ?,?,?)", ( directory, template_name, st.session_state.user["username"],datetime.now()))
	conn.commit()
	conn.close()
 
def get_templates():
	conn = sqlite3.connect(WORKING_DATABASE)
	cursor = conn.cursor()
	
	# Fetch only the password for the given username
	cursor.execute('SELECT * FROM AOR_Template_Files ORDER BY uploaded_on DESC')
	result = cursor.fetchall()
	conn.close()
	
	return result


def save_to_file(filename,text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Add text to PDF, splitting long text into multiple lines
    for line in text.split('\n'):
        encoded_line = line.encode('latin-1', 'ignore').decode('latin-1')  # Ignore unsupported characters
        pdf.multi_cell(200, 10, txt=encoded_line)
        
    UPLOAD_DIRECTORY = os.path.join(cwd, "uploaded_files")
    if not os.path.exists(UPLOAD_DIRECTORY):
        os.makedirs(UPLOAD_DIRECTORY)
    # Save the PDF
    file_path = os.path.join(UPLOAD_DIRECTORY, filename+".pdf")
    pdf.output(file_path)
    return file_path
