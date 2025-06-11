import datetime
import sys
from types import SimpleNamespace
from unittest.mock import patch
from streamlit.testing.v1 import AppTest


class _FakeGenerativeModel:
    def __init__(self, *args, **kwargs):
        pass

    def generate_content(self, prompt):
        return MockResponse("stub")


def _fake_configure(api_key=None):
    pass

if "google.generativeai" not in sys.modules:
    stub = SimpleNamespace(
        GenerativeModel=_FakeGenerativeModel, configure=_fake_configure
    )
    google_mod = sys.modules.setdefault("google", SimpleNamespace())
    google_mod.generativeai = stub
    sys.modules["google.generativeai"] = stub

class MockResponse:
    def __init__(self, text):
        self.text = text

@patch("google.generativeai.GenerativeModel.generate_content")
def test_Chatbot(genai_create):
    at = AppTest.from_file("Chatbot.py").run()
    assert not at.exception
    at.chat_input[0].set_value("Do you know any jokes?").run()
    assert at.info[0].value == "Please add your Google API key to continue."

    JOKE = "Why did the chicken cross the road? To get to the other side."
    genai_create.return_value = MockResponse(JOKE)
    at.text_input(key="chatbot_api_key").set_value("sk-...")
    at.chat_input[0].set_value("Do you know any jokes?").run()
    print(at)
    assert at.chat_message[1].markdown[0].value == "Do you know any jokes?"
    assert at.chat_message[2].markdown[0].value == JOKE
    assert at.chat_message[2].avatar == "assistant"
    assert not at.exception

@patch("google.generativeai.GenerativeModel.generate_content")
def test_Quickstart(genai_create):
    at = AppTest.from_file("pages/3_Langchain_Quickstart.py").run()
    assert at.info[0].value == "Please add your Google API key to continue."

    RESPONSE = "1. The best way to learn how to code is by practicing..."
    genai_create.return_value = MockResponse(RESPONSE)
    at.sidebar.text_input[0].set_value("sk-...")
    at.button[0].set_value(True).run()
    print(at)
    assert at.info[0].value == RESPONSE
