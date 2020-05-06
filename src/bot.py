import asyncio
import os

import discord
from discord.ext import commands

import checks
import helpers
from game import Game

if os.path.isfile('../.env'):
    from dotenv import load_dotenv
    load_dotenv()

bot = commands.Bot(os.environ['PREFIX'])
game = None
game_state_lock = asyncio.Lock()


# Events

@bot.event
async def on_ready():
    global game
    game = Game(await bot.fetch_guild(int(os.environ['GUILD'])))
    print('Ready!')


@bot.event
async def on_voice_state_update(member, before, after):
    if member.bot or not game.is_running():
        return

    # If user joined current voice and game is running
    if before.channel != game.voice_channel and after.channel == game.voice_channel:
        await helpers.try_set_prefix(member, game.get_prefix(member))

    # If user left current voice
    elif before.channel == game.voice_channel and after.channel != game.voice_channel:
        await helpers.try_remove_prefix(member)


# Global checks

@bot.check
async def globally_check_server(ctx):
    return ctx.guild is None or ctx.guild == game.guild


# Commands

@bot.command()
async def ping(ctx):
    await ctx.send(f':ping_pong: {round(bot.latency * 1000)}ms')


@bot.command()
@checks.voice_only()
async def start(ctx):
    async with game_state_lock:
        if game.is_running():
            await ctx.send('Игра уже запущена')
            return
        await game.start_game(ctx.author.voice.channel, ctx.author)

        # Set prefixes
        await ctx.send(':gear: Раздаем префиксы...')
        for p in game.players:
            await helpers.try_set_prefix(p.member, game.get_prefix(p.member))

        await ctx.send(
            f'Игра начинается в **{game.voice_channel}**! Ведущий - {ctx.author.mention}')


@bot.command()
@commands.guild_only()
async def finish(ctx):
    async with game_state_lock:
        if not game.is_running():
            await ctx.send('Игра не запущена')
            return

        # Remove prefixes
        await ctx.send(':gear: Убираем префиксы...')
        for p in game.voice_channel.members:
            await helpers.try_remove_prefix(p)

        await ctx.send(f'Игра в **{game.voice_channel}** завершена')
        await game.finish_game()


# Commands for debugging

@bot.command(aliases=['debug_sp'])
@commands.is_owner()
async def debug_set_prefix(ctx, member: discord.Member, prefix: str):
    await helpers.try_set_prefix(member, prefix)


@bot.command(aliases=['debug_rp'])
@commands.is_owner()
async def debug_remove_prefix(ctx, member: discord.Member):
    await helpers.try_remove_prefix(member)


bot.run(os.environ['TOKEN'])
