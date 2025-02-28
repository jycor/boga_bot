import discord
from discord.ext import commands
from discord import File
from datetime import datetime, timezone, timedelta, date
import asyncio

import consts
import ask_cmd
import urban_dict
import youtube
import boba_math
import daily_task
import japan_cmd
import uwuify
import gifgenerate
import twitch_random
import weather
import chatgpt_api
import sql_queries
import mc_server

pst = timezone(timedelta(hours=-8))
intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents, help_command=None)

debug_channel = None

@bot.event
async def on_ready():
  
  print("I'm in")
  print(bot.user)

  global start_time
  start_time = datetime.now()

  daily_task.send_daily_msg.start(bot)

  global debug_channel
  debug_channel = bot.get_channel(consts.DEBUG_CH_ID)
  await debug_channel.send("I am alive")


@bot.command()
async def sync(ctx):
  print("sync command")
  if ctx.author.id == consts.ALEX_ID or ctx.author.id == consts.JAMES_ID:
    await bot.tree.sync()
    await ctx.send('Command tree synced.')
  else:
    await ctx.send('You must be the owner to use this command!')


@bot.command()
async def echo(ctx, *, args):
  if ctx.author.id == consts.ALEX_ID or ctx.author.id == consts.JAMES_ID:
    if ctx.channel.id == consts.DEBUG_CH_ID:
      newctx = bot.get_channel(consts.GENERAL_CH_ID)
      await newctx.send(args)
    else:
      await ctx.send('it broke')

@bot.hybrid_command(name="minecraft", description="Check the status of the Wack Wrappers minecraft server.")
async def minecraft(ctx):
  response = mc_server.get_details()
  await ctx.send(response)

@bot.hybrid_command(name="help", description="a helpful command")
async def help(ctx):
  await ctx.send('ask <@{0}>'.format(consts.ALEX_ID))


@bot.hybrid_command(name="urban", description="define a word")
async def urban(ctx, term: str = commands.parameter(default="", description="type any word or phrase")):
  term = term.strip().lower()
  if len(term) > 0:
    try:
      result = urban_dict.define(term)
      await ctx.send(result)
      sql_queries.log_command("urban")
    except:
      await ctx.send("I don't know what {0} is".format(term))
  else:
    await ctx.send("Please add a phrase")


@bot.hybrid_command(name="randword", description="random urban dictionary word")
async def randword(ctx):
  result = urban_dict.random()
  await ctx.send(result)
  sql_queries.log_command("randword")


@bot.hybrid_command(name="wordoftheday", description="daily word")
async def wordoftheday(ctx):
  result = urban_dict.word_of_the_day()
  await ctx.send(result)
  sql_queries.log_command("wordoftheday")


@bot.hybrid_command(name="meme", description="Watch this video.")
async def meme_video(ctx):
  await ctx.send("https://www.instagram.com/p/Ct_icUhuYn7/")
  sql_queries.log_command("meme")


@bot.hybrid_command(name="japan", description="wack wrapper japan countdown")
async def japan(ctx):
  days, hours, minutes, seconds = japan_cmd.countdown(datetime(2025, 1, 1, tzinfo=pst))
  msg = "{0} days, {1} hours, {2} minutes, {3} seconds till Japan :airplane: :flag_jp:".format(days, hours, minutes, seconds)
  await ctx.send(msg)
  sql_queries.log_command("japan")


@bot.hybrid_command(name="bye-wayne", description="wack wrapper wayne exit countdown")
async def wayne(ctx):
  days, hours, minutes, seconds = japan_cmd.countdown(datetime(2024, 8, 11, tzinfo=pst))
  msg = "{0} days, {1} hours, {2} minutes, {3} seconds till Wayne fricks himself in Misery :student: :pill: ".format(days, hours, minutes, seconds)
  await ctx.send(msg)
  sql_queries.log_command("bye-wayne")


@bot.hybrid_command(name="uptime", description="time when bot started")
async def uptime(ctx):
  global start_time
  diff = datetime.now() - start_time
  days = diff.days
  hours, rem = divmod(diff.seconds, 3600)
  minutes, seconds = divmod(rem, 60)
  diff_str = "{0} days, {1} hours, {2} minutes, {3} seconds".format(days, hours, minutes, seconds)
  await ctx.send("I was started at `{0}`.\nI've been up for `{1}`.".format(start_time, diff_str))
  sql_queries.log_command("uptime")


@bot.hybrid_command(name="ask", description="truthfully answers a question with yes or no")
async def ask(ctx, question: str):
  res = ask_cmd.ask(question)
  await ctx.send(res)
  sql_queries.log_command("ask")


@bot.hybrid_command(name="boba", description="Calculate price based off boba")
async def boba(ctx, value: str):
  res = boba_math.calc(value)
  await ctx.send(res)
  sql_queries.log_command("boba")


@bot.hybrid_command(name="yt-trending", description="#1 trending video on youtube")
async def yt_trending(ctx):
  res = youtube.get_trending()
  msg = "The #1 trending video on youtube is:\n{0}".format(res)
  await ctx.send(msg)
  sql_queries.log_command("yt-trending")


@bot.hybrid_command(name="uwu", description="uwuify sentence given in user response.")
async def uwu(ctx, *, args):
  res = uwuify.uwuify(args)
  await ctx.send(res)
  sql_queries.log_command("uwu")


@bot.hybrid_command(name="twitch-streamer", description="Give you a random streamer currently live on Twitch.")
async def twitch_streamer(ctx):
  res = twitch_random.generate_channel()
  await ctx.send(res)
  sql_queries.log_command("twitch-streamer")


@bot.hybrid_command(name="weather", description="Get the current weather in a specific location.")
async def current_weather(ctx, *, args):
  res, condition, icon, err = weather.get_weather(args)
  if err:
    await ctx.send(res)
    global debug_channel
    await debug_channel.send("Error: {0}".format(err))
  else:
    response = "{0}\nThe weather is currently [**{1}**](https:{2})".format(res, condition.upper(), icon)
    await ctx.send(response)
    sql_queries.log_command("weather")


@bot.hybrid_command(name="image", description="Generate an image based on a prompt. THIS COSTS MONEY.")
async def image(ctx, *, args):
  await ctx.defer()
  response, err = chatgpt_api.generate_image(ctx.author.id, args)
  await ctx.send(response)
  sql_queries.log_command("image")
  if err:
    global debug_channel
    await debug_channel.send("Error: {0}".format(err))


@bot.hybrid_command(name="bill", description="Get the current bill for the user. If no user is specified, it will default to the author.")
async def bill(ctx, user: discord.Member=None, month: int=None, year: int=None): 
  # Gets bill of user from specific month/year if passed by user, else get current month/year. 

  today = datetime.now()
  
  user_id = ctx.author.id if user is None else user.id
  month = today.month if month is None else month
  year = today.year if year is None else year

  if month < 1 or month > 12:
    await ctx.send("Please send a valid date.")
    return

  if year < 2024 or year > today.year:
    await ctx.send("Please send a valid date.")
    return

  response = sql_queries.generate_user_bill(user_id, month, year)
  
  await ctx.send(response)
  sql_queries.log_command("bill")


@bot.hybrid_command(name="usage", description="Check usage of commands of Boga bot so far.")
async def usage(ctx):
  await ctx.defer()
  res = sql_queries.get_command_usage()
  await ctx.send(res)


@bot.hybrid_command(name="goon", description="Enter the gooniverse")
async def goon(ctx):
  await ctx.send("https://tenor.com/view/jarvis-iron-man-goon-gif-5902471035652079804")

@bot.hybrid_command(name="jiawei", description="Where's the japan video Jiawei?")
async def roast_jiawei(ctx):
  japan_return_date = date(2023, 9, 7)
  today = date.today()

  num_days = abs((today - japan_return_date).days)

  await ctx.send("It's been about {0} days that <@!{1}> has stalled making the Japan video :JiaweiOOO:".format(num_days, consts.JIAWEI_ID))


@bot.event
async def on_message(message):
  # ignore messages from the bot
  if message.author.bot:
    return
  
  # possible text commands
  cmd = message.content.split(" ")[0]
  match cmd:
    case "/sync":
      ctx = await bot.get_context(message)
      await sync(ctx)
      return
    case "/echo":
      ctx = await bot.get_context(message)
      await echo(ctx, args=message.content[6:])
      return
    case "/randgif": # Leave in case of integration testing. Won't make as hybrid command cause just used for daily announcement. 
      ctx = await bot.get_context(message)
      gif = gifgenerate.generate_gif()
      if gif:
        await message.channel.send(gif)
      else:
        await message.channel.send("Gif failed.")
      return
    case "/forget":
      ctx = await bot.get_context(message)
      if ctx.author.id == consts.ALEX_ID or ctx.author.id == consts.JAMES_ID:
        chatgpt_api.clear_history()
        await message.channel.send("Cleared chat history.")
      return
    case "/statement":
      response = sql_queries.generate_statement()
      await message.channel.send(response)
      return

  # ignore messages that don't mention the bot
  if not bot.user.mentioned_in(message):
    return

  if message.author.id == consts.ALEX_ID: # Jiawei roast message if he tries to mention the bot. 
    await message.channel.send("Please finish the Japan video <@!{0}>".format(consts.JIAWEI_ID))
    return

  ctx = await bot.get_context(message)  
  async with ctx.typing():
    response, err = await chatgpt_api.generate_chatgpt_response(message.author.id, message.content)
    if err:
      global debug_channel
      await debug_channel.send("Error: {0}".format(err))
    
  for i in range(0, len(response), chatgpt_api.DISCORD_MSG_LIMIT):
    async with ctx.typing():
      await message.channel.send(response[i:i+chatgpt_api.DISCORD_MSG_LIMIT], reference=message)
      await asyncio.sleep(0.5) # delay to make it feel more natural; can remove
  
  sql_queries.log_command("chatgpt")
  

bot.run(consts.API_KEY)
