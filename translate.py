# Q&A Chatbot
import google.generativeai as genai
import streamlit as st
import os

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Function to load Gemini model and get response
def get_gemini_response(question):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(question)
    return response.text

# Initialize our Streamlit app
st.set_page_config(page_title="Q&A Demo")
st.header("Langchain Application")

input_text = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

# If ask button is clicked, get response
if submit and input_text:
    response = get_gemini_response(input_text)
    st.subheader("The Response is")
    st.write(response)
