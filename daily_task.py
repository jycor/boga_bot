import os
from datetime import time, datetime, timedelta
from zoneinfo import ZoneInfo

import urban_dict

from discord.ext import commands, tasks

# If no tzinfo is given then UTC is assumed.
pst = ZoneInfo(key='America/Los_Angeles')
t = time(hour=8, tzinfo=pst)
# USE THIS FOR DEBUGGING
# dt = datetime.now() + timedelta(seconds=10)
# t = time(hour=dt.hour, minute=dt.minute, second=dt.second, tzinfo=pst)
japan_date = datetime(2025, 1, 1, tzinfo=pst)

class TaskCog(commands.Cog):

  def __init__(self, bot):
    self.bot = bot
    self.my_task.start()

  def cog_unload(self):
    self.my_task.cancel()

  @tasks.loop(time=t)
  async def my_task(self):
    my_secret = int(os.environ['DISCORD_CHANNEL_SECRET'])
    ctx = self.bot.get_channel(my_secret)  # this is general chat.

    greeting = "Good morning everyone!"
    daily_word = "The Word of the Day is:\n{0}".format(urban_dict.word_of_the_day())
    msg = "{0}\n{1}".format(greeting, daily_word)

    await ctx.send(msg)

  def generate_countdown(): # Keep in case of 
    today = datetime.today().astimezone(pst)

    diff = japan_date - today
    days = diff.days
    hours, rem = divmod(diff.seconds, 3600)
    minutes, seconds = divmod(rem, 60)

    return days, hours, minutes, seconds
