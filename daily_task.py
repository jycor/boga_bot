from discord.ext import tasks
from zoneinfo import ZoneInfo
from datetime import datetime, timedelta, time

import consts
import youtube
import urban_dict
import gifgenerate

pst = ZoneInfo(key='America/Los_Angeles')
daily_msg_time = time(hour=8, tzinfo=pst)


# USE THIS FOR TESTING
# dt = datetime.now() + timedelta(seconds=10)
# daily_msg_time = time(hour=dt.hour, minute=dt.minute, second=dt.second, tzinfo=pst)

# ANOTHER DEBUG METHOD IN CASE ABOVE NOT WORKING: 
# @tasks.loop(seconds=5.0)

@tasks.loop(time=daily_msg_time)
async def send_daily_msg(bot):
  ctx = bot.get_channel(consts.GENERAL_CH_ID)

  urban_dict.reset_word_of_the_day()

  greeting = "Good morning everyone!"
  daily_word_msg = "The Word of the Day is:\n{0}".format(urban_dict.word_of_the_day())
  daily_yt_vid = "The #1 trending video on YouTube is:\n{0}".format(youtube.get_trending())
  msg = "{0}\n{1}\n{2}".format(greeting, daily_word_msg, daily_yt_vid)
  gif_url = gifgenerate.generate_gif()

  await ctx.send(msg)
  await ctx.send(gif_url)
