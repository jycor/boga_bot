from math import ceil
def boba_calc(amount: str):
    try: 
        int_amt = int(amount)
        conversion = ceil(int_amt / 6.50)
        return "That'd cost you about {0} bobas.".format(conversion)
    except:
        return ("Incorrect amount sent, please fix : o")
