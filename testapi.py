import streamlit as st
import requests
from fastapi import FastAPI
from pydantic import BaseModel

# Create a FastAPI app
app = FastAPI()

# Create a Pydantic model for the input data
class Item(BaseModel):
    name: str
    price: float


# FastAPI endpoint
@app.get("/api/get_item")
async def get_item(name: str):
    return {"response": name}

# Streamlit UI
st.title("Streamlit App with REST API")

# Input fields
name = st.text_input("Enter item name")
price = st.number_input("Enter item price", min_value=0.01, step=0.01)

if st.button("Create Item"):
    # Make a POST request to the FastAPI endpoint
    response = requests.post(
        "http://localhost:8000/api/item",
        json={"name": name, "price": price}
    )
    
    if response.status_code == 200:
        st.success(response.json()["message"])
    else:
        st.error("Failed to create item")

# To run both Streamlit and FastAPI
import uvicorn
import threading

def run_fastapi():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    # Start FastAPI in a separate thread
    threading.Thread(target=run_fastapi, daemon=True).start()
    
  