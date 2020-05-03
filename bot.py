import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()
bot = commands.Bot(os.environ['PREFIX'])


@bot.event
async def on_ready():
    print('Ready')


@bot.command()
async def ping(ctx):
    await ctx.send(f':ping_pong:  {round(bot.latency * 1000)}ms')


bot.run(os.environ['TOKEN'])
