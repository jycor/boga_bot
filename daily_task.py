from discord.ext import tasks

from datetime import datetime, timezone, timedelta, time

import consts
import youtube
import urban_dict
import gifgenerate

pst = timezone(timedelta(hours=-8))
daily_msg_time = time(hour=8, tzinfo=pst)

# USE THIS FOR TESTING
# dt = datetime.now() + timedelta(seconds=10)
# daily_msg_time = time(hour=dt.hour, minute=dt.minute, second=dt.second, tzinfo=pst)

@tasks.loop(time=daily_msg_time)
async def send_daily_msg(bot):
  ctx = bot.get_channel(consts.GENERAL_CH_ID)

  urban_dict.reset_word_of_the_day()

  greeting = "Good morning everyone!"
  daily_word_msg = "The Word of the Day is:\n{0}".format(urban_dict.word_of_the_day())
  daily_yt_vid = "The #1 trending video on YouTube is:\n{0}".format(youtube.get_trending())
  daily_gif = "The Gif of the Day is:\n{0}".format(gifgenerate.generate_gif())
  msg = "{0}\n{1}\n{2}\n{3}".format(greeting, daily_word_msg, daily_yt_vid, daily_gif)

  await ctx.send(msg)
