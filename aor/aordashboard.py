import streamlit as st
from PIL import Image
import os
cwd = os.getcwd()

def prototype_application():
    # Display image from a URL
    UPLOAD_DIRECTORY = os.path.join(cwd, 'resources\\')
    # Load the image from a local file
    image = Image.open(UPLOAD_DIRECTORY+"aordashboard.jpg")  # Replace with your image file path
    # Display the image
    st.image(image,  use_column_width=True)
