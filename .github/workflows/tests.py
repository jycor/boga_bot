import sys
import os

main_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add the main directory to the system path
sys.path.append(main_dir)
import boba_math
import gifgenerate
import pytest


def test_boba():
    assert boba_math.calc("6") == "It's basically free! Why are you bothering with this command?"

def test_gif_generate():
    assert gifgenerate.generate_gif() != None