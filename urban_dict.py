import os
import requests

urban_dict_key = os.environ['URBAN_DICT_API_KEY']

url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
rand_url = "https://api.urbandictionary.com/v0/random"

headers = {
  'x-rapidapi-key': urban_dict_key,
  'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com"
}

def format(entry):
  word = entry['word']
  defn = entry['definition']
  example = entry['example']
  author = entry['author']
  result = "```\nWord:\n{0}\n\nDefinition:\n{1}\n\nExample:\n{2}\n\nAuthor: {3}```".format(word, defn, example, author)
  return result


def define(term):
  querystring = {"term": term}
  response = requests.request("GET", url, headers=headers, params=querystring)
  resp_json = response.json()
  result = format(resp_json['list'][0])
  return result


def random():
  response = requests.request("GET", rand_url, headers=headers)
  resp_json = response.json()
  result = format(resp_json['list'][0])
  return result


def word_of_the_day():
  url = "https://mashape-community-urban-dictionary.p.rapidapi.com/words"
  response = requests.request("GET", url, headers=headers)
  resp_json = response.json()
  word = resp_json['word']
  return word