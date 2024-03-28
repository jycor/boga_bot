import requests
import json
from consts import UNSPLASH_KEY

def get_photo(query):
    try:
        res = requests.get(
        "https://api.unsplash.com/photos/random?client_id=%s&per_page=1&query=%s" % (UNSPLASH_KEY, query))
        if res.status_code == 200:
            results = json.loads(res.content)
            return results['urls']['raw']
        else:
            return ("Request failed. Please try command again.")
    except:
        return ("Error. Try again later.")

