from openai import OpenAI
import streamlit as st

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="project_helper_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
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
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)

if st.session_state.get("summary"):
    st.write("### Final Topic")
    st.write(st.session_state["summary"])

summary_button_placeholder = st.empty()
if (
    st.session_state.get("summary") is None
    and summary_button_placeholder.button("I'm excited about this topic", key="excited_button")
):
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()
    client = OpenAI(api_key=openai_api_key)
    summary_messages = st.session_state.messages + [
        {
            "role": "user",
            "content": (
                "Please summarize the project idea we've discussed in 2-3 paragraphs suitable "
                "for a middle school student."
            ),
        }
    ]
    summary_response = client.chat.completions.create(
        model="gpt-3.5-turbo", messages=summary_messages
    )
    summary = summary_response.choices[0].message.content
    st.session_state["summary"] = summary
    summary_button_placeholder.empty()
    st.write("### Final Topic")
    st.write(summary)
