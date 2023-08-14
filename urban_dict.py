import os
import requests

urban_dict_key = os.environ['URBAN_DICT_API_KEY']

url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"

headers = {
  'x-rapidapi-key': urban_dict_key,
  'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com"
}


def define(term):
  querystring = {"term": term}
  response = requests.request("GET", url, headers=headers, params=querystring)
  resp_json = response.json()
  defn = resp_json['list'][0]['definition']
  return defn