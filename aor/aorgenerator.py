import streamlit as st
import os
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


def generate_aor(selected_item):   
    # This is a placeholder function. Replace with your actual text generation logic
    texts = {
        "Template 1": "This is the generated text for Template 1.",
        "Template 2": "Here's some text generated for Template 2.",
        "Template 3": "And this is what we generated for Template 3."
    }
    
    response = client.chat.completions.create(
    	model="gpt-4o-mini",  
    	messages=[
			{
			"role": "user",
            "content": texts.get(selected_item, "No text available for this Template."),
			}
    	])
	
    return response.choices[0].message.content


def prototype_application():
	#insert the code
 
	st.title("AOR Generator")

	# Dropdown for item selection
	selected_item = st.selectbox("Select a Template:", ["Template 1", "Template 2", "Template 3"])

	# Generate button
	if st.button("Generate"):
		generated_aor = generate_aor(selected_item)
		st.session_state.text_area_value = generated_aor

	title = st.text_input("AOR Title:")
	# Text area
	text_area = st.text_area("Generated Text:", value=st.session_state.get('text_area_value', ''), height=500)
	
 	# Submit button
	if st.button("Submit"):
		save_to_db(title,text_area)
		st.success(f"AOR {title} has been saved successfully.")
    
    
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
  

def save_to_db(title,generated_aor):
	# collect data from template
	conn = sqlite3.connect(WORKING_DATABASE)
	cursor = conn.cursor()
	now = datetime.now()  # Using ISO format for date
	cursor.execute("INSERT INTO AOR VALUES (?, ?, ?,?)", (title, generated_aor, st.session_state.user["username"], datetime.now()))
	conn.commit()
	conn.close()
 