import os
import requests

urban_secret = os.environ['URBAN_SECRET']

url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"

headers = {
  'x-rapidapi-key': urban_secret,
  'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com"
}


def define(term):
  querystring = {"term": term}
  response = requests.request("GET", url, headers=headers, params=querystring)
  resp_json = response.json()
  defn = resp_json['list'][0]['definition']
  return defn