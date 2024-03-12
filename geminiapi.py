import pathlib
import textwrap
from consts import GOOGLE_API_KEY
# Used to securely store your API key
import google.generativeai as genai

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])
MAX_HIST_LENGTH = 10

def generate_gemini_response(user_input: str):
    global chat
    response = chat.send_message(user_input)
    if len(chat.history) > MAX_HIST_LENGTH:
        chat.history = chat.history[-MAX_HIST_LENGTH:]
    return response.text


