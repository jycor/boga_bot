# TODO: come up with a way to log database errors?
import sqlite3
from datetime import datetime

PROG_CHR = "*"
MISS_CHR = "-"

DB_NAME = 'boga.db'

# Create database on startup
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()
cursor.execute((
    "CREATE TABLE IF NOT EXISTS costs("
    "    user_id INTEGER,"
    "    date TEXT,"
    "    type TEXT,"
    "    cost REAL"
    ")"
))
conn.commit()

cursor.execute((
    "CREATE INDEX IF NOT EXISTS date_index ON costs (date)"
))
conn.commit()

cursor.execute((
    "CREATE INDEX IF NOT EXISTS user_id_index ON costs (user_id)"
))
conn.commit()

cursor.execute((
    "CREATE TABLE IF NOT EXISTS usage("
    "    command TEXT,"
    "    count INTEGER"
    ")"
))
conn.commit()

cursor.execute((
    "CREATE TABLE IF NOT EXISTS track_roll("
    "    user_id INTEGER PRIMARY KEY,"
    "    roll INTEGER,"
    "    streak INTEGER DEFAULT 0"
    ")"
))
conn.commit()

cursor.execute((
    "CREATE TABLE IF NOT EXISTS boga_bucks("
    "    user_id INTEGER PRIMARY KEY,"
    "    boga_bucks INTEGER"
    ")"
))
conn.commit()

cursor.close()
conn.close()

def log_command(command: str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute((
        "SELECT command\n"
        "FROM usage\n"
        "WHERE command=?"), 
        (command,)
    )

    rows = cursor.fetchall()
    if len(rows) == 0:
        cursor.execute((
        "INSERT INTO usage(\n"
        "   command,\n"
        "   count\n"
        ") VALUES(?, 0)"
        ), (command, )
        )
        conn.commit()
    
    cursor.execute((
        "UPDATE usage\n"
        "SET\n"
        "    count = count + 1\n"
        "WHERE command=?"
        ), (command,)
    )
    conn.commit()

    cursor.close()
    conn.close()

def get_command_usage():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute((
            "SELECT *\n"
            "FROM usage\n"
            "ORDER BY\n"
            "    count DESC,\n"
            "    command ASC\n"
            )
        )

        rows = cursor.fetchall()

        cursor.execute((
            "SELECT \n"
            "    SUM(count)\n"
            "FROM usage"
            )
        )
        
        total = cursor.fetchall()[0][0]
        conn.close()
        
        res = "```"

        for row in rows:
            
            percent = round((row[1] / total) * 100, 2)
            progress = round((row[1] / total) * 10)
            progress_bar = (PROG_CHR * progress) + (MISS_CHR * (10 - progress))

            res += "/{:15} [{}] {}%\n".format(row[0], progress_bar, str(percent))
        
        res += "```"

        
        
        return res
    except:
        return "There was an issue generating usage, please try again later."

def log_cost(user_id: int, type: str, cost: float):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute((
        "INSERT INTO costs(\n"
        "   user_id,\n"
        "   date,\n"
        "   type,\n"
        "   cost\n"
        ") VALUES(?, ?, ?, ?)"
        ), (user_id, str(datetime.now()), type, cost)
    )
    conn.commit()
    cursor.close()
    conn.close()

# apply_roll updates the track_roll and boga_bucks tables with the user's roll amount if they haven't already rolled today.

def apply_roll(user_id: int, roll: int):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute((
        "SELECT\n"
        "   user_id,\n"
        "   roll\n"
        "   FROM track_roll\n"
        "   WHERE user_id=?"
        ), (user_id,)
    )

    return_message = ""
    rows = cursor.fetchall()
    if len(rows) == 0: # new roll, hasn't rolled before. 
        cursor.execute((
            "INSERT INTO track_roll(\n"
            "   user_id,\n"
            "   roll,\n"
            "   streak\n"
            ") VALUES(?, ?, ?)"
            ), (user_id, 1, 0)
        )
        conn.commit()

        cursor.execute((
            "INSERT INTO boga_bucks(\n"
            "   user_id,\n"
            "   boga_bucks\n"
            ") VALUES(?, ?)"
            ), (user_id, roll)
        )
        conn.commit()
        return_message = "You earned `{}` Boga Bucks!".format(roll)
    else: #user has rolled at some point, check if they rolled this roll.
        if rows[0][1] == 1:
            return_message = "You already rolled today. Try again after reset! (12:00am PST)"
        else:
            cursor.execute((
                "UPDATE track_roll\n"
                "SET\n"
                "   roll = 1\n"
                "WHERE user_id = ?"
                ), (user_id,)
            )
            conn.commit()
            
            # update boga bucks table with new roll for boga_bucks field.
            cursor.execute((
                "UPDATE boga_bucks\n"
                "SET\n"
                "    boga_bucks = boga_bucks + ?\n"
                "WHERE user_id = ?"
                ), (roll, user_id)
            )
            conn.commit()
            return_message = "You earned `{}` Boga Bucks!".format(roll)
            
    cursor.close()
    conn.close()

    return return_message

def reset_rolls(): # On 12:00am PST, reset all user rolls to 0.
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # First update streaks for users who rolled (roll = 1)
    cursor.execute((
        "UPDATE track_roll\n"
        "SET streak = streak + 1\n"
        "WHERE roll = 1"
    ))
    conn.commit()

    # Reset streaks to 0 for users who didn't roll (roll = 0)
    cursor.execute((
        "UPDATE track_roll\n"
        "SET streak = 0\n"
        "WHERE roll = 0"
    ))
    conn.commit()

    # Finally, reset all rolls back to 0
    cursor.execute((
        "UPDATE track_roll\n"
        "SET roll = 0"
    ))
    conn.commit()
    
    cursor.close()
    conn.close()

def get_boga_bucks(user_id: int):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute((
        "SELECT\n"
        "   boga_bucks\n"
        "FROM boga_bucks\n"
        "WHERE user_id=?"
        ), (user_id,)
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    if len(rows) == 0:
        return 0
    
    return rows[0][0]

def add_boga_bucks(user_id: int, amount: int):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute((
                "UPDATE boga_bucks\n"
                "SET\n"
                "    boga_bucks = boga_bucks + ?\n"
                "WHERE user_id = ?"
                ), (amount, user_id)
            )
    conn.commit()
    cursor.close()
    conn.close()

def get_leaderboard():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute((
        "SELECT\n"
        "   user_id,\n"
        "   boga_bucks\n"
        "FROM boga_bucks\n"
        "ORDER BY\n"
        "   boga_bucks DESC\n"
    ))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    if len(rows) == 0:
        return "Nobody has rolled yet!"
    
    response = "Boga Bucks Leaderboard:\n"
    curr = 1
    for row in rows: 
        response += "{0}. <@{1}>: `{2}`\n".format(curr, row[0], row[1])
        curr += 1
    return response

def generate_user_bill(user_id: int, month=None, year=None): 
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    start_date = datetime(year=year, month=month, day=1)
    end_month = month + 1 if month != 12 else 1
    end_year = year + 1 if end_month == 1 else year
    end_date = datetime(year=end_year, month=end_month, day=1)

    cursor.execute((
        "SELECT\n"
        "    sum(cost)\n"
        "FROM costs\n"
        "WHERE user_id=?\n"
        "AND date >=?\n"
        "AND date <=?\n"
        ), (user_id, start_date, end_date)
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    
    total_cost = rows[0][0] if rows[0][0] is not None else 0

    return "<@!{}> owes `${}` for `{}/{}`".format(user_id, total_cost, month, year)

def generate_statement():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute((
        "SELECT\n"
        "    user_id,\n"
        "    sum(cost)\n"
        "FROM costs\n"
        "GROUP BY \n"
        "    user_id\n"
        "ORDER BY\n"
        "    sum(cost) DESC,\n"
        "    user_id"
        )
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    if len(rows) == 0:
        return "Nobody has used the bot yet"

    res = "# Statement Summary starting from 04/2024\n\n"

    total = 0
    for row in rows:
        tmp = "<@!{}> owes `${}`\n".format(row[0], row[1])
        res += tmp
        total += row[1]
    
    res += "\nTotal: `${}`".format(total)
    return res