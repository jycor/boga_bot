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

def generate_chatgpt_response(user_id: int, query: str):
    global client
    global chat_history
    
    try:
        user_query = {"role": "user", "content": query}
        chat_history.append(user_query)

        gpt_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=chat_history,
        )

        update_token_cost(user_id, gpt_response.usage.completion_tokens, gpt_response.usage.prompt_tokens)

        response = gpt_response.choices[0].message.content

        if len(response) > DISCORD_MSG_LIMIT:
            response = response[:DISCORD_MSG_LIMIT-3] + "..."

        gpt_response = {"role": "assistant", "content": response}
        chat_history.append(gpt_response)

        if len(chat_history) > MAX_CHAT_LEN:
            chat_history = chat_history[-MAX_CHAT_LEN:]
        
        return response
    except Exception as err:
        return err

def generate_image(user_id: int, query: str):
    global client

    # temporarily disable image generation to save on costs
    # update_img_cost(user_id)
    # return "image gen is disabled for testing"

    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=query,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        update_img_cost(user_id)

        image_url = response.data[0].url
        return image_url
    except Exception as err:
        return err

# TODO: consider moving this to a separate file
# TODO: come up with a way to log database errors?
import sqlite3
DB_NAME = 'boga.db'
IMG_COST = 0.04
INPUT_TOKEN_COST = 0.50 / 1_000_000
OUTPUT_TOKEN_COST = 1.50 / 1_000_000

# Create database on startup
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()
cursor.execute((
    "CREATE TABLE IF NOT EXISTS costs("
    "    user_id INTEGER PRIMARY KEY,"
    "    num_imgs INTEGER,"
    "    num_in_tokens INTEGER,"
    "    num_out_tokens INTEGER,"
    "    img_cost REAL,"
    "    token_cost REAL,"
    "    total_cost REAL"
    ")"
))
cursor.close()

# TODO: run these database queries asynchronously
# TODO: add a way to clear a user's costs

def update_img_cost(user_id: int):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # check if user exists, add if they don't
    cursor.execute((
        "SELECT user_id\n"
        "FROM costs\n"
        "WHERE user_id=?"), 
        (user_id,)
    )
    rows = cursor.fetchall()
    if len(rows) == 0:
        cursor.execute((
            "INSERT INTO costs(\n"
            "   user_id,\n"
            "   num_imgs,\n"
            "   num_in_tokens,\n"
            "   num_out_tokens,\n"
            "   img_cost,\n"
            "   token_cost,\n"
            "   total_cost\n"
            ") VALUES(?, 0, 0, 0, 0, 0, 0)"
            ), (user_id,)
        )
        conn.commit()

    cursor.execute((
        "UPDATE costs SET\n"
        "    num_imgs = num_imgs + 1,\n"
        "    img_cost = img_cost + ?,\n"
        "    total_cost = total_cost + ?\n"
        "WHERE user_id=?"
        ), (IMG_COST, IMG_COST, user_id,)
    )
    conn.commit()
    cursor.close()

def update_token_cost(user_id: int, num_input_tokens: int, num_output_tokens: int):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # check if user exists, add if they don't
    cursor.execute((
        "SELECT user_id\n"
        "FROM costs\n"
        "WHERE user_id=?"
        ), (user_id,)
    )
    rows = cursor.fetchall()
    if len(rows) == 0:
        cursor.execute((
            "INSERT INTO costs(\n"
            "   user_id,\n"
            "   num_imgs,\n"
            "   num_in_tokens,\n"
            "   num_out_tokens,\n"
            "   img_cost,\n"
            "   token_cost,\n"
            "   total_cost\n"
            ") VALUES(?, 0, 0, 0, 0, 0, 0)"
            ), (user_id,)
        )
        conn.commit()

    total_cost = num_input_tokens * INPUT_TOKEN_COST + num_output_tokens * OUTPUT_TOKEN_COST
    cursor.execute((
        "UPDATE costs\n"
        "SET\n"
        "    num_in_tokens = num_in_tokens + ?,\n"
        "    num_out_tokens = num_out_tokens + ?,\n"
        "    token_cost = token_cost + ?,\n"
        "    total_cost = total_cost + ?\n"
        "WHERE user_id=?"
        ), (num_input_tokens, num_output_tokens, total_cost, total_cost, user_id,)
    )
    conn.commit()
    cursor.close()

def generate_user_bill(user_id: int):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute((
        "SELECT\n"
        "    img_cost,\n"
        "    token_cost,\n"
        "    total_cost\n"
        "FROM costs\n"
        "WHERE user_id=?\n"
        ), (user_id,)
    )
    rows = cursor.fetchall()
    cursor.close()

    if len(rows) == 0:
        return "You've never used the bot before!"
    
    img, token, total = rows[0][0], rows[0][1], rows[0][2]
    return (
        "```"
        "Billing Summary:\n"
        "\tImage Cost: ${0:.2f}\n"
        "\tToken Cost: ${1:.2f}\n"
        "\tTotal Cost: ${2:.2f}"
        "```"
    ).format(img, token, total)

def generate_statement():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute((
        "SELECT\n"
        "    user_id,\n"
        "    total_cost\n"
        "FROM costs\n"
        )
    )
    rows = cursor.fetchall()
    cursor.close()

    if len(rows) == 0:
        return "Nobody has used the bot yet"
    
    res = ""
    total = 0
    for row in rows:
        tmp = "<@!{}> owes ${}\n".format(row[0], row[1])
        res += tmp
        total += row[1]
    res += "Total: ${}".format(total)
    return res