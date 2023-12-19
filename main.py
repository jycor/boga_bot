import os
import discord
from datetime import datetime
from discord.ext import commands

import ask_cmd
import urban_dict
from daily_task import TaskCog
from datetime import datetime
from boba_math import boba_calc
import ask_cmd

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents, help_command=None)

ALEX_ID = os.environ['ALEX_USER_ID']
JAMES_ID = os.environ['JAMES_USER_ID']

@bot.event
async def on_ready():
  print("I'm in")
  print(bot.user)

  global start_time
  start_time = datetime.now()

  debug_channel_id = int(os.environ['DEBUG_CHANNEL_ID'])
  debug_channel = bot.get_channel(debug_channel_id)
  await debug_channel.send("I am alive")

  cog = TaskCog(bot)
  await bot.add_cog(cog, override=False)


@bot.command()
async def sync(ctx):
  print("sync command")
  if ctx.author.id == int(ALEX_ID) or ctx.author.id == int(JAMES_ID):
    await bot.tree.sync()
    await ctx.send('Command tree synced.')
  else:
    await ctx.send('You must be the owner to use this command!')


@bot.hybrid_command(name="help", description="a helpful command")
async def help(ctx):
  await ctx.send('ask <@{0}>'.format(str(ALEX_ID)))


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


@bot.hybrid_command(name="meme", description="Watch this video.")
async def meme_video(ctx):
  await ctx.send("https://www.instagram.com/p/Ct_icUhuYn7/")


@bot.hybrid_command(name="japan", description="wack wrapper japan countdown")
async def japan(ctx):
  days, hours, minutes, seconds = TaskCog.generate_countdown()
  msg = "{0} days, {1} hours, {2} minutes, {3} seconds till Japan :airplane: :flag_jp:".format(days, hours, minutes, seconds)
  await ctx.send(msg)


@bot.hybrid_command(name="ask", description="truthfully answers a question with yes or no")
async def ask(ctx, question: str):
  res = ask_cmd.ask(question)
  await ctx.send(res)

@bot.hybrid_command(name="boba", description="Calculate price based off boba")
async def boba(ctx, value: str):
  result = boba_calc(value)
  await ctx.send(result)

@bot.hybrid_command(name="bully", description="Mess around with somebody. ")
async def bully(ctx, name: str):
  result = bully(name)
  await ctx.send(result)

my_secret = os.environ['DISCORD_BOT_API_KEY']
bot.run(my_secret)
