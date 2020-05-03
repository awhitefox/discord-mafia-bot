from discord.ext import commands


def voice_only():
    def predicate(ctx):
        return ctx.guild is not None and ctx.author.voice is not None
    return commands.check(predicate)
