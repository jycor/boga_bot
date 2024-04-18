import discord
from discord.ext import commands
from discord import File
from datetime import datetime

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
    except:
      await ctx.send("I don't know what {0} is".format(term))
  else:
    await ctx.send("Please add a phrase")


@bot.hybrid_command(name="randword", description="random urban dictionary word")
async def randword(ctx):
  result = urban_dict.random()
  await ctx.send(result)


@bot.hybrid_command(name="wordoftheday", description="daily word")
async def wordoftheday(ctx):
  result = urban_dict.word_of_the_day()
  await ctx.send(result)


@bot.hybrid_command(name="meme", description="Watch this video.")
async def meme_video(ctx):
  await ctx.send("https://www.instagram.com/p/Ct_icUhuYn7/")


@bot.hybrid_command(name="japan", description="wack wrapper japan countdown")
async def japan(ctx):
  days, hours, minutes, seconds = japan_cmd.countdown()
  msg = "{0} days, {1} hours, {2} minutes, {3} seconds till Japan :airplane: :flag_jp:".format(days, hours, minutes, seconds)
  await ctx.send(msg)


@bot.hybrid_command(name="uptime", description="time when bot started")
async def uptime(ctx):
  global start_time
  diff = datetime.now() - start_time
  days = diff.days
  hours, rem = divmod(diff.seconds, 3600)
  minutes, seconds = divmod(rem, 60)
  diff_str = "{0} days, {1} hours, {2} minutes, {3} seconds".format(days, hours, minutes, seconds)
  await ctx.send("I was started at `{0}`.\nI've been up for `{1}`.".format(start_time, diff_str))


@bot.hybrid_command(name="ask", description="truthfully answers a question with yes or no")
async def ask(ctx, question: str):
  res = ask_cmd.ask(question)
  await ctx.send(res)


@bot.hybrid_command(name="boba", description="Calculate price based off boba")
async def boba(ctx, value: str):
  res = boba_math.calc(value)
  await ctx.send(res)


@bot.hybrid_command(name="yt-trending", description="#1 trending video on youtube")
async def yt_trending(ctx):
  res = youtube.get_trending()
  msg = "The #1 trending video on youtube is:\n{0}".format(res)
  await ctx.send(msg)

@bot.hybrid_command(name="uwu", description="uwuify sentence given in user response.")
async def uwu(ctx, *, args):
  res = uwuify.uwuify(args)
  await ctx.send(res)

@bot.hybrid_command(name="twitch-streamer", description="Give you a random streamer currently live on Twitch.")
async def twitch_streamer(ctx):
  res = twitch_random.generate_channel()
  await ctx.send(res)

@bot.hybrid_command(name="weather", description="Get the current weather in a specific location.")
async def current_weather(ctx, *, args):
  res, condition, icon = weather.get_weather(args)
  response = "{0}\nThe weather is currently [**{1}**](https:{2})".format(res, condition.upper(), icon)
  await ctx.send(response)

@bot.hybrid_command(name="image", description="Generate an image based on a prompt. THIS COSTS MONEY.")
async def image(ctx, *, args):
  response, err = chatgpt_api.generate_image(ctx.author.id, args)
  await ctx.send(response)
  if err:
    global debug_channel
    await debug_channel.send("Error: {0}".format(err))

@bot.hybrid_command(name="bill", description="Get the current bill for the user. If no user is specified, it will default to the author.")
async def bill(ctx, user: discord.Member=None):
  response = chatgpt_api.generate_user_bill(ctx.author.id if user is None else user.id)
  await ctx.send(response)

# TODO: should this command be public?
# @bot.hybrid_command(name="statement", description="Prints everyone's bill.")
# async def statement(ctx):
#   response = chatgpt_api.generate_statement()
#   await ctx.send(response)

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
    case "/image":
      response = chatgpt_api.generate_image(message.author.id, message.content[7:])
      await message.channel.send(response)
      return
    case "/bill":
      # as a text command, this will always use the author
      response = chatgpt_api.generate_user_bill(message.author.id)
      await message.channel.send(response)
      return
    case "/statement":
      response = chatgpt_api.generate_statement()
      await message.channel.send(response)
      return

  # ignore messages that don't mention the bot
  if not bot.user.mentioned_in(message):
    return

  response, err = chatgpt_api.generate_chatgpt_response(message.author.id, message.content)
  await message.channel.send(response, reference=message)

  if err:
    global debug_channel
    await debug_channel.send("Error: {0}".format(err))
  

bot.run(consts.API_KEY)
