from consts import GOOGLE_API_KEY
import google.generativeai as genai

DISCORD_MSG_LIMIT = 2000

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')
safety_settings = [
    {
        "category": "HARM_CATEGORY_DANGEROUS",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]

chat = model.start_chat(history=[])
MAX_HIST_LENGTH = 10

def clear_history():
    global chat
    chat.history = []

def generate_gemini_response(user_input: str):
    global chat
    global safety_settings
    try:
        response = chat.send_message(user_input, safety_settings=safety_settings)
    except Exception as e:
        print(e)
        return "I'm sorry, I can't do that right now."
    if len(chat.history) > MAX_HIST_LENGTH:
        chat.history = chat.history[-MAX_HIST_LENGTH:]
    if len(response.text) > DISCORD_MSG_LIMIT:
        return response.text[:DISCORD_MSG_LIMIT-3] + "..."
    return response.text
