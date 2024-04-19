import requests
import json
from consts import WEATHER_API_KEY
from pprint import pprint

def get_weather(location):
    try:
        res = requests.get("https://api.weatherapi.com/v1/current.json?q=%s&key=%s" % (location, WEATHER_API_KEY))
        if res.status_code == 200:
            results = json.loads(res.content)
            response = "The temperature in **" + location.strip() + "** is currently **" + str(results['current']['temp_f']) + " F**."
            return response, results['current']['condition']['text'].lower(), results['current']['condition']['icon'], None
        else:
            return "Request failed. Please try fixing the location or a new one.", None, None, "Received status code: {}".format(res.status_code)
    except Exception as err:
        return "Error. Try a different location.", None, None, err
