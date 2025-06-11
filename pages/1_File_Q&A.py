import streamlit as st
import google.generativeai as genai

with st.sidebar:
    google_api_key = st.text_input("Google API Key", key="file_qa_api_key", type="password")
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/pages/1_File_Q%26A.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

st.title("📝 File Q&A with Gemini")
uploaded_file = st.file_uploader("Upload an article", type=("txt", "md"))
question = st.text_input(
    "Ask something about the article",
    placeholder="Can you give me a short summary?",
    disabled=not uploaded_file,
)

if uploaded_file and question and not google_api_key:
    st.info("Please add your Google API key to continue.")

if uploaded_file and question and google_api_key:
    article = uploaded_file.read().decode()
    genai.configure(api_key=google_api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")
    prompt = f"{article}\n\n{question}"
    response = model.generate_content(prompt)
    st.write("### Answer")
    st.write(response.text)
