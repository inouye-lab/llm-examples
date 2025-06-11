import google.generativeai as genai
import streamlit as st

with st.sidebar:
    google_api_key = st.text_input("Google API Key", key="project_helper_api_key", type="password")
    "[Get a Google API key](https://makersuite.google.com/app/apikey)"
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/pages/6_Middle_school_project_helper.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

st.title("🧑‍🎓 Middle School Project Helper")
st.caption("💡 A chatbot for brainstorming project ideas")

if "summary" not in st.session_state:
    st.session_state["summary"] = None

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "assistant",
            "content": (
                "Hello! I'm ProjectPro, your friendly AI research buddy. "
                "I once helped organize a school science fair and love turning curiosity into exciting projects. "
                "Tell me a bit about what you enjoy or any ideas you already have."
            ),
        }
    ]

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

if st.session_state.get("summary"):
    st.write("### Final Topic")
    st.write(st.session_state["summary"])

if st.session_state.get("summary") is None and st.button("I'm excited about this topic"):
    if not google_api_key:
        st.info("Please add your Google API key to continue.")
        st.stop()
    genai.configure(api_key=google_api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")
    summary_messages = st.session_state.messages + [
        {
            "role": "user",
            "content": (
                "Please summarize the project idea we've discussed in 2-3 paragraphs suitable "
                "for a middle school student."
            ),
        }
    ]
    prompt_text = "\n".join(f"{m['role']}: {m['content']}" for m in summary_messages)
    summary_response = model.generate_content(prompt_text)
    summary = summary_response.text
    st.session_state["summary"] = summary
    st.write("### Final Topic")
    st.write(summary)
