import streamlit as st
from duckduckgo_search import DDGS
import google.generativeai as genai

with st.sidebar:
    google_api_key = st.text_input(
        "Google API Key", key="langchain_search_api_key", type="password"
    )
    "[Get a Google API key](https://makersuite.google.com/app/apikey)"
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/pages/2_Chat_with_search.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

st.title("🔎 Chat with search")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi, I'm a chatbot who can search the web. How can I help you?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input(placeholder="Who won the Women's U.S. Open in 2018?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    if not google_api_key:
        st.info("Please add your Google API key to continue.")
        st.stop()

    with DDGS() as ddgs:
        results = ddgs.text(prompt, max_results=5)
    snippets = "\n".join(r["body"] for r in results)

    genai.configure(api_key=google_api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")
    context = f"Use the following search results to answer the question.\n{snippets}"
    response = model.generate_content(f"{context}\n\nQuestion: {prompt}")
    st.session_state.messages.append({"role": "assistant", "content": response.text})
    st.chat_message("assistant").write(response.text)
