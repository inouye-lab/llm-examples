import google.generativeai as genai
import streamlit as st

with st.sidebar:
    google_api_key = st.text_input("Google API Key", key="chatbot_api_key", type="password")
    "[Get a Google API key](https://makersuite.google.com/app/apikey)"
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

st.title("💬 Chatbot")
st.caption("🚀 A Streamlit chatbot powered by Gemini 2.5 Flash")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not google_api_key:
        st.info("Please add your Google API key to continue.")
        st.stop()

    genai.configure(api_key=google_api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    prompt_text = "\n".join(
        f"{m['role']}: {m['content']}" for m in st.session_state.messages
    )
    response = model.generate_content(prompt_text)
    msg = response.text
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
