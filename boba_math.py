import re

pattern = r'^\$?\d+(,\d{3})*(\.[0-9]{2})?$'

from math import ceil
def boba_calc(amount: str):
    
    if not re.match(pattern, amount):
        return "Please use a proper price: " + amount
    
    converted_amount = amount.replace("$", "").replace(",", "")
    amt = float(converted_amount) # checks if decimal is in string and should resolve.
    if amt < 6.50: 
        return "It's basically free! Why are you bothering with this command?" 
    
    conversion = ceil(int(amt) / 6.50)

    if "$" not in amount:
        amount = "$" + amount

    return "When you pay {0}, that's about {1} bobas! Isn't that concerning?".format(amount, conversion)
    
    
