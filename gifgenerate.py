import requests
import json
import random
from consts import GIF_API_KEY

gif_api_key = GIF_API_KEY
lmt=15
ckey = "boga-bot"

def generate_gif():
    res = requests.get(
    "https://tenor.googleapis.com/v2/featured?&key=%s&client_key=%s&limit=%s" % (gif_api_key, ckey,  lmt))
    if res.status_code == 200:
        # load the GIFs using the urls for the smaller GIF sizes
        results = json.loads(res.content)['results']
        gif = random.choice(results)
        return (gif['media_formats']['gif']['url'])
    else:
        return None