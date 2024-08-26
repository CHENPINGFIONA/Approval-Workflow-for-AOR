import streamlit as st
import pandas as pd
import numpy as np

# Set title of the app
st.title('Approval Workflow for AOR')

# Add a text input widget
name = st.text_input("Enter your name:")

# Display the input name
if name:
    st.write(f"Hello, {name}!")

# Add a button and a response
if st.button('Say Hello'):
    st.write("Hello from Streamlit!")

# Add a slider widget
x = st.slider('Select a number', 0, 100, 25)
st.write(f'You selected {x}')

# Display a DataFrame
df = pd.DataFrame(
    np.random.randn(10, 3),
    columns=['Column 1', 'Column 2', 'Column 3']
)
st.write("Here is a random dataframe:")
st.dataframe(df)

# Show a line chart
st.line_chart(df)

