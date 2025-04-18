from discord.ext import tasks
from zoneinfo import ZoneInfo
from datetime import datetime, timedelta, time
import sql_queries
import consts


pst = ZoneInfo(key='America/Los_Angeles')
daily_msg_time = time(hour=0, tzinfo=pst)

# USE THIS FOR TESTING
# dt = datetime.now() + timedelta(seconds=10)
# daily_msg_time = time(hour=dt.hour, minute=dt.minute, second=dt.second, tzinfo=pst)

# ANOTHER DEBUG METHOD IN CASE ABOVE NOT WORKING: 
# @tasks.loop(seconds=5.0)

@tasks.loop(time=daily_msg_time)
async def reset_db_task(bot):
  ctx = bot.get_channel(consts.GENERAL_CH_ID) # Change this to real channel to send message to. 
  sql_queries.reset_user_rolls()
  await ctx.send("Reset time, everyone can reroll again!")
  # reset db logic here, every day it will reset db at 12:00am PST. 