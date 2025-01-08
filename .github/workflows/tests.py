import sys
import os

main_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))

# Add the main directory to the system path
sys.path.append(main_dir)
import boba_math
import gifgenerate
import chatgpt_api
import youtube
import pytest
import weather
import urban_dict
import twitch_random


def test_gif_generate():
    assert gifgenerate.generate_gif() != None

def test_youtube():
    youtube.get_trending()

def test_weather():
    assert weather.get_weather("LA")[0] not in ["Error. Try a different location.", "Request failed. Please try fixing the location or a new one."]

def test_define():
    urban_dict.define("test")

def test_random():
    urban_dict.random()

def test_twitch():
    twitch_random.generate_channel()