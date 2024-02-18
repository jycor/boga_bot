from discord.ext import tasks

from datetime import datetime, timezone, timedelta, time

from consts import GENERAL_CH_ID, DEBUG_CH_ID
from youtube import get_trending
from urban_dict import word_of_the_day, reset_word_of_the_day

pst = timezone(timedelta(hours=-8))
daily_msg_time = time(hour=8, tzinfo=pst)

# USE THIS FOR TESTING
# dt = datetime.now() + timedelta(seconds=10)
# daily_msg_time = time(hour=dt.hour, minute=dt.minute, second=dt.second, tzinfo=pst)

@tasks.loop(time=daily_msg_time)
async def send_daily_msg(bot):
  ctx = bot.get_channel(GENERAL_CH_ID)

  reset_word_of_the_day()

  greeting = "Good morning everyone!"
  daily_word_msg = "The Word of the Day is:\n{0}".format(word_of_the_day())
  daily_yt_vid = "The #1 trending video on YouTube is:\n{0}".format(get_trending())
  msg = "{0}\n{1}\n{2}".format(greeting, daily_word_msg, daily_yt_vid)

  await ctx.send(msg)
