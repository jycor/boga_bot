import random

# TODO: add more variety to responses; potentially through a context-free grammar
def ask(question: str):
    odds = random.random()
    if odds < 0.10:
        answer = "maybe"
    elif odds < 0.55:
        answer = "yes"
    else:
        answer = "no"
    return "> {0}\n{1}".format(question, answer)