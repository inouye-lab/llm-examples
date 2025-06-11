import streamlit as st
import google.generativeai as genai

st.title("🦜🔗 Quickstart App")

with st.sidebar:
    google_api_key = st.text_input("Google API Key", type="password")
    "[Get a Google API key](https://makersuite.google.com/app/apikey)"


def generate_response(input_text):
    genai.configure(api_key=google_api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(input_text)
    st.info(response.text)


with st.form("my_form"):
    text = st.text_area("Enter text:", "What are 3 key advice for learning how to code?")
    submitted = st.form_submit_button("Submit")
    if not google_api_key:
        st.info("Please add your Google API key to continue.")
    elif submitted:
        generate_response(text)
