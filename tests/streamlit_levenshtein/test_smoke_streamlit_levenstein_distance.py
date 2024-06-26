from streamlit.testing.v1 import AppTest


def test_smoke_page_input():
    at = AppTest.from_file('../../streamlit_app/pages/levenshtein_distance.py')
    at.run()
    assert not at.exception

    at.text_input[0].input("bok")
    at.button[0].click().run()
    assert at.session_state["correct_word"] == 'book'
