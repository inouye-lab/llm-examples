import streamlit as st
import google.generativeai as genai

st.title("🦜🔗 Blog Outline Generator App")

google_api_key = st.sidebar.text_input("Google API Key", type="password")


def blog_outline(topic: str):
    genai.configure(api_key=google_api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")
    template = (
        "As an experienced data scientist and technical writer, generate an outline for a blog about {topic}."
    )
    prompt = template.format(topic=topic)
    response = model.generate_content(prompt)
    return st.info(response.text)


with st.form("myform"):
    topic_text = st.text_input("Enter prompt:", "")
    submitted = st.form_submit_button("Submit")
    if not google_api_key:
        st.info("Please add your Google API key to continue.")
    elif submitted:
        blog_outline(topic_text)
