import discord
changed_names = dict()


async def try_set_prefix(member: discord.Member, prefix):
    # TODO ADD check if player has prefix for some reason
    try:
        changed_names[member.id] = member.display_name
        await member.edit(
            nick=f'[{prefix}] {member.display_name}'[:32])  # 32 is the discord name limit
        return True
    except discord.errors.Forbidden:
        return False


async def try_remove_prefix(member):
    try:
        if member.id in changed_names:
            await member.edit(nick=changed_names.pop(member.id))
        return True
    except discord.errors.Forbidden:
        return False
