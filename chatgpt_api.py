from openai import OpenAI
from consts import OPENAI_API_KEY

client = OpenAI(
    api_key=OPENAI_API_KEY
)

chat_history = [] 
MAX_CHAT_LEN = 20
DISCORD_MSG_LIMIT = 2000

def clear_history():
    global chat_history
    chat_history = []

def generate_chatgpt_response(query: str):
    global client
    global chat_history
    
    try:
        user_query = {"role": "user", "content": query}
        chat_history.append(user_query)

        gpt_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=chat_history,
        )

        response = gpt_response.choices[0].message.content
        
        if len(response) > DISCORD_MSG_LIMIT:
            response = response[:DISCORD_MSG_LIMIT-3] + "..."

        gpt_response = {"role": "assistant", "content": response}
        chat_history.append(gpt_response)

        if len(chat_history) > MAX_CHAT_LEN:
            chat_history = chat_history[-MAX_CHAT_LEN:]
        
        return response
    except:
        return "There was an issue with your query, please try again later."

def generate_image(query: str):
    global client

    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=query,
            size="1024x1024",
            quality="standard",
            n=1,
        )

        image_url = response.data[0].url
        return image_url
    except:
        return "There was an error generating your image, please try again later."