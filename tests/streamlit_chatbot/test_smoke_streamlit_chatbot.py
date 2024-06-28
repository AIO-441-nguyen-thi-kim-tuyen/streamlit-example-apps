import hugchat.login
import os
from unittest.mock import patch
from streamlit.testing.v1 import AppTest
import json
from streamlit_app.pages.chatbot import generate_response


def test_smoke_page():
    at = AppTest.from_file('../../streamlit_app/pages/chatbot.py')
    at.run()
    assert not at.exception

    email = "test@example.com"
    password = "password123"

    at.text_input[0].input(email)
    at.text_input[1].input(password)
    at.run()
    assert len(at.success) == 1
    assert at.session_state.messages[0]["content"] == "How may I help you?"


class Cookies:
    def __init__(self, cookie_dict):
        self.cookies = cookie_dict

    def get_dict(self):
        return self.cookies


def test_generate_response():
    email = "test@example.com"
    password = "password123"
    prompt = "What is the capital of Vietnam?"
    with patch.object(hugchat.login.Login, 'login') as mock_login, patch.object(hugchat.login.Login,
                                                                                '_sign_in_with_email') as email_sign_in:
        # Opening JSON file
        cookie_path_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "usercookies", "test@example.com.json"))
        f = open(cookie_path_dir)
        cookie_dict = json.load(f)
        # print("cookie_dict:%s" % cookie_dict)
        mock_login.return_value = Cookies(cookie_dict)
        email_sign_in.return_value = None
        response = generate_response(prompt, email, password)
        # print("response:%s" % response.text)

    assert response.text == "The capital of Vietnam is Hanoi."

# def test_smoke_response():
#     at = AppTest.from_file('../../streamlit_app/pages/chatbot.py')
#     at.run()
#     assert not at.exception
#     with (patch.object(hugchat.login.Login, 'login') as mock_login, patch.object(hugchat.login.Login,
#                                                                                 '_sign_in_with_email') as email_sign_in):
#         # Opening JSON file
#         cookie_path_dir = os.path.abspath(
#             os.path.join(os.path.dirname(__file__), "usercookies", "test@example.com.json"))
#         f = open(cookie_path_dir)
#         cookie_dict = json.load(f)
#         # print("cookie_dict:%s" % cookie_dict)
#         mock_login.return_value = Cookies(cookie_dict)
#         email_sign_in.return_value = None
#
#         prompt = "What is the capital of Vietnam?"
#         at.chat_input[0].set_value(prompt)
#         at.run()
#
#     print(at.session_state.messages)
#     assert not at.exception
