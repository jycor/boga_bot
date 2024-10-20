from openai import OpenAI
from consts import OPENAI_API_KEY
import sql_queries

client = OpenAI(
    api_key=OPENAI_API_KEY
)

chat_history = [] 
MAX_CHAT_LEN = 20
DISCORD_MSG_LIMIT = 2000
IMG_COST = 0.04
INPUT_TOKEN_COST = 0.15 / 1_000_000
OUTPUT_TOKEN_COST = 0.60 / 1_000_000

def clear_history():
    global chat_history
    chat_history = []

async def generate_chatgpt_response(user_id: int, query: str):
    global chat_history
    
    try:
        user_query = {"role": "user", "content": query}
        chat_history.append(user_query)

        gpt_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=chat_history,
        )

        completion_cost =  INPUT_TOKEN_COST * gpt_response.usage.completion_tokens
        prompt_cost = OUTPUT_TOKEN_COST * gpt_response.usage.prompt_tokens

        sql_queries.log_cost(user_id, "text", completion_cost + prompt_cost)

        response = gpt_response.choices[0].message.content

        gpt_response = {"role": "assistant", "content": response}
        chat_history.append(gpt_response)

        if len(chat_history) > MAX_CHAT_LEN:
            chat_history = chat_history[-MAX_CHAT_LEN:]
        
        return response, None
    except Exception as err:
        return "There was an issue with your query, please try again later.", err

def generate_image(user_id: int, query: str):

    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=query,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        sql_queries.log_cost(user_id, "image", IMG_COST)

        image_url = response.data[0].url
        return image_url, None
    except Exception as err:
        return "There was an error generating your image, please try again later.", err