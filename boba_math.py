from math import ceil
def boba_calc(amount: str):
    try:
        converted_amount = amount.replace("$", "").replace(",", "")
        int_amt = int(float(converted_amount)) # checks if decimal is in string and should resolve. 
        conversion = ceil(int_amt / 6.50)

        if "$" not in amount:
            amount = "$" + amount

        return "When you pay {0}, that's about {1} bobas! Isn't that concerning?".format(amount, conversion)
    except:
        return "Please use a proper dollar amount to calculate bobas."
    
