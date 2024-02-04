import os
from datetime import time, datetime, timedelta
import pytz

import urban_dict
import youtube

from discord.ext import commands, tasks

# If no tzinfo is given then UTC is assumed.
pst = pytz.timezone('US/Pacific')
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
    my_secret = int(os.environ['WACK_WRAPPERS_CHANNEL_ID'])
    ctx = self.bot.get_channel(my_secret)  # this is general chat.
    urban_dict.reset_word_of_the_day()

    greeting = "Good morning everyone!"
    daily_word_msg = "The Word of the Day is:\n{0}".format(urban_dict.word_of_the_day())
    daily_yt_vid = "The #1 trending video on YouTube is:\n{0}".format(youtube.get_trending())
    msg = "{0}\n{1}\n{2}".format(greeting, daily_word_msg, daily_yt_vid)

    await ctx.send(msg)

  def generate_countdown(): # Keep in case of 
    today = datetime.today().astimezone(pst)

    diff = japan_date - today
    days = diff.days
    hours, rem = divmod(diff.seconds, 3600)
    minutes, seconds = divmod(rem, 60)

    return days, hours, minutes, seconds
