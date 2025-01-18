import boba_math
import gifgenerate
import pytest


def test_boba():
    assert boba_math.calc("6") == "It's basically free! Why are you bothering with this command?"

def test_gif_generate():
    assert gifgenerate.generate_gif() != None