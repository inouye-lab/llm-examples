import google.generativeai as genai
import streamlit as st
from streamlit_feedback import streamlit_feedback
import trubrics

with st.sidebar:
    google_api_key = st.text_input("Google API Key", key="feedback_api_key", type="password")
    "[Get a Google API key](https://makersuite.google.com/app/apikey)"
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/pages/5_Chat_with_user_feedback.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

st.title("📝 Chat with feedback (Trubrics)")

"""
In this example, we're using [streamlit-feedback](https://github.com/trubrics/streamlit-feedback) and Trubrics to collect and store feedback
from the user about the LLM responses.
"""

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "How can I help you? Leave feedback to help me improve!"}
    ]
if "response" not in st.session_state:
    st.session_state["response"] = None

messages = st.session_state.messages
for msg in messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input(placeholder="Tell me a joke about sharks"):
    messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    if not google_api_key:
        st.info("Please add your Google API key to continue.")
        st.stop()
    genai.configure(api_key=google_api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")
    prompt_text = "\n".join(f"{m['role']}: {m['content']}" for m in messages)
    response = model.generate_content(prompt_text)
    st.session_state["response"] = response.text
    with st.chat_message("assistant"):
        messages.append({"role": "assistant", "content": st.session_state["response"]})
        st.write(st.session_state["response"])

if st.session_state["response"]:
    feedback = streamlit_feedback(
        feedback_type="thumbs",
        optional_text_label="[Optional] Please provide an explanation",
        key=f"feedback_{len(messages)}",
    )
    # This app is logging feedback to Trubrics backend, but you can send it anywhere.
    # The return value of streamlit_feedback() is just a dict.
    # Configure your own account at https://trubrics.streamlit.app/
    if feedback and "TRUBRICS_EMAIL" in st.secrets:
        config = trubrics.init(
            email=st.secrets.TRUBRICS_EMAIL,
            password=st.secrets.TRUBRICS_PASSWORD,
        )
        collection = trubrics.collect(
            component_name="default",
            model="gemini-2.5-flash",
            response=feedback,
            metadata={"chat": messages},
        )
        trubrics.save(config, collection)
        st.toast("Feedback recorded!", icon="📝")
