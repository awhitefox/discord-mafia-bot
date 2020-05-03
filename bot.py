import os
import random

import discord
from discord.ext import commands
from dotenv import load_dotenv

import checks
import helpers

load_dotenv()
bot = commands.Bot(os.environ['PREFIX'])

current_voice = None
current_players = []


# Events

@bot.event
async def on_ready():
    print('Ready')


@bot.event
async def on_voice_state_update(member, before, after):
    if member.bot:
        return

    # If user joined current voice and game is running
    if current_voice is not None and before.channel != current_voice and after.channel == current_voice:
        if member in current_players:
            i = current_players.index(member)
            prefix = str(i) if i != 0 else 'В'
            await helpers.set_prefix(member, prefix)
        else:
            await helpers.set_prefix(member, 'Н')
            await member.edit(mute=True)

    # If user left current voice
    elif before.channel == current_voice and after.channel != current_voice:
        await helpers.remove_prefix(member)
        await member.edit(mute=False)


# Commands

@bot.command()
async def ping(ctx):
    await ctx.send(f':ping_pong:  {round(bot.latency * 1000)}ms')


@bot.command()
@checks.voice_only()
async def start(ctx):
    global current_voice, current_players
    if current_voice is not None:
        await ctx.send('Игра уже запущена')
        return
    current_voice = ctx.author.voice.channel

    # Put everybody in voice channel except bots and message author
    current_players.extend(filter(lambda x: not (x.bot or x == ctx.author), current_voice.members))
    # Shuffle players and put author on first place
    random.shuffle(current_players)
    current_players.insert(0, ctx.author)

    await ctx.send(f'Игра начинается в **{current_voice}**! Ведуший - {ctx.author.mention}')

    await helpers.set_prefix(ctx.author, 'В')
    for i in range(1, len(current_players)):
        await helpers.set_prefix(current_players[i], str(i))


@bot.command()
@commands.guild_only()
async def finish(ctx):
    global current_voice
    if current_voice is None:
        await ctx.send('Игра не запущена')
        return

    for p in current_voice.members:
        await helpers.remove_prefix(p)
    await ctx.send(f'Игра в **{current_voice}** завершена')

    current_voice = None
    current_players.clear()


# Commands for debugging

@bot.command(aliases=['debug_sp'])
@commands.is_owner()
async def debug_set_prefix(ctx, member: discord.Member, prefix: str):
    await helpers.set_prefix(member, prefix)


@bot.command(aliases=['debug_rp'])
@commands.is_owner()
async def debug_remove_prefix(ctx, member: discord.Member):
    await helpers.remove_prefix(member)


bot.run(os.environ['TOKEN'])
