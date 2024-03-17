def uwuify(sentence):
  """Converts a sentence to uwu-speak.

  Args:
    sentence: The sentence to convert.

  Returns:
    The uwu-ified sentence.
  """

  # Define a dictionary of uwu-speak replacements.
  replacements = {
      "l": "w",
      "r": "w",
      "th": "f",
      "v": "bw",
      "n": "ny",
      "m": "my",
      "o": "owo",
      "a": "aw",
      "e": "ew",
      "i": "iw",
      "u": "uwu",
      "y": "wy",
  }

  # Replace all the letters in the sentence with their uwu-speak equivalents.
  uwu_sentence = ""
  for letter in sentence:
    if letter in replacements:
      uwu_sentence += replacements[letter]
    else:
      uwu_sentence += letter

  # Add some uwu-speak punctuation.
  uwu_sentence = uwu_sentence.replace(".", " nya~")
  uwu_sentence = uwu_sentence.replace("!", " >w<")
  uwu_sentence = uwu_sentence.replace("?", " owo?")

  # Return the uwu-ified sentence.
  return uwu_sentence