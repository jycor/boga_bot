import os
import random
import discord
from discord.ext import commands

import urban_dict
from daily_task import TaskCog

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents, help_command=None)

ALEX_ID = os.environ['ALEX_USER_ID']
JAMES_ID = os.environ['JAMES_USER_ID']

is_bullying = False
bullyee_id = None


@bot.event
async def on_ready():
  print("I'm in")
  print(bot.user)

  debug_channel_id = int(os.environ['DEBUG_CHANNEL_ID'])
  debug_channel = bot.get_channel(debug_channel_id)
  await debug_channel.send("I am alive")

  cog = TaskCog(bot)
  await bot.add_cog(cog, override=False)


@bot.event
async def on_message(msg):
  global is_bullying, bullyee_id
  if not is_bullying or msg.author.id == bot.user.id or msg.author.id != bullyee_id:
    await bot.process_commands(msg)
    return
  if msg.content[0] == '/':
    await bot.process_commands(msg)
    return
  await msg.reply("hey fucker")


@bot.hybrid_command(name="bully", description="bully this person")
async def bully(ctx, id: discord.Member):
  global is_bullying, bullyee_id
  is_bullying = True
  bullyee_id = id
  print(bullyee_id)


#@bot.hybrid_command(name="stop-bully", description="no more bullying")
@bot.command()
async def stop_bully(ctx):
  global is_bullying, bullyee_id
  is_bullying = False
  bullyee_id = None
  print("no more bullying")


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
      defn = urban_dict.define(term)
      await ctx.send(term + " is: \n" + defn)
    except:
      await ctx.send("I don't know what {0} is".format(term))
  else:
    await ctx.send("Please add a phrase")


@bot.hybrid_command(name="meme", description="Watch this video.")
async def meme_video(ctx):
  await ctx.send("https://www.instagram.com/p/Ct_icUhuYn7/")


@bot.hybrid_command(name="japan", description="wack wrapper japan countdown")
async def japan(ctx):
  days, hours, minutes, seconds = TaskCog.generate_countdown()
  await ctx.send(
    str(days) + " days, " + str(hours) + " hours, " + str(minutes) +
    " minutes, " + str(seconds) + " seconds till Japan :airplane: :flag_jp:")


@bot.hybrid_command(name="ask",
                    description="truthfully answers a question with yes or no")
async def ask(ctx, question: str):
  if random.random() < 0.5:
    await ctx.send("> {0}\nyes".format(question))
  else:
    await ctx.send("> {0}\nno".format(question))


@bot.hybrid_command()
async def boga(ctx, arg: str):
  await ctx.send("BOGABOGA")


@bot.hybrid_command(name='testing', description='test command with parameters')
async def test_command(ctx, param1: str, param2: int = 69):
  print("TESTING")
  await ctx.send(param1 + str(param2))


@bot.command()
async def test(ctx):
  print("TESTING2")
  await ctx.reply("AMONGUS")

my_secret = os.environ['DISCORD_BOT_API_KEY']
bot.run(my_secret)
