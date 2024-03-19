import requests
import random
from datetime import datetime, timedelta
from consts import TWITCH_API_KEY, TWITCH_SECRET

expiry_time = None
access_token = None

TWITCH_SEARCH_URL = 'https://api.twitch.tv/helix/streams?first=50&type=live'
TWITCH_AUTH_URL = 'https://id.twitch.tv/oauth2/token'

AUTH_PARAMS = {
        'client_id': TWITCH_API_KEY,
        'client_secret': TWITCH_SECRET,
        'grant_type': 'client_credentials'
}

def refresh_token():
    global expiry_time
    global access_token

    auth_call = requests.post(url=TWITCH_AUTH_URL, params=AUTH_PARAMS)
    expiry = int(auth_call.json()['expires_in'])

    expiry_time = datetime.now() + timedelta(seconds=expiry)
    access_token = auth_call.json()['access_token']

def generate_channel():
    global expiry_time
    global access_token
    if not expiry_time or expiry_time < datetime.now():
        refresh_token()
        print("Refreshed token!")   
    
    header = {
        'Client-ID' : TWITCH_API_KEY,
        'Authorization' :  "Bearer " + access_token
    }
    
    streamer_data = requests.get(TWITCH_SEARCH_URL, headers = header).json()['data']
    random_streamer = random.choice(streamer_data)['user_name']

    return "Your random streamer is:\nhttps://www.twitch.tv/" + random_streamer

    
