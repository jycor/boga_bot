import os
from datetime import time, datetime
from zoneinfo import ZoneInfo
from discord.ext import commands, tasks

# If no tzinfo is given then UTC is assumed.
pst = ZoneInfo(key='America/Los_Angeles')
time = time(hour=8, minute=0, tzinfo=pst)
japan_date = datetime(2023, 8, 23, tzinfo=pst)

class TaskCog(commands.Cog):

  def __init__(self, bot):
    self.bot = bot
    self.my_task.start()

  def cog_unload(self):
    self.my_task.cancel()

  @tasks.loop(time=time)
  async def my_task(self):
    my_secret = int(os.environ['DISCORD_CHANNEL_SECRET'])
    ctx = self.bot.get_channel(my_secret)  # this is general chat.
    today = datetime.today().astimezone(pst)
    if today < japan_date:
      message = str((japan_date - today).days) + " more days till Japan. :airplane: :flag_jp:"
      await ctx.send(message)
    else:
      # TODO: We are in Japan for x more days?
      await ctx.send("We are in Japan!!!")

  def generate_countdown():
    today = datetime.today().astimezone(pst)

    diff = japan_date - today
    days = diff.days
    hours, rem = divmod(diff.seconds, 3600)
    minutes, seconds = divmod(rem, 60)

    return days, hours, minutes, seconds
