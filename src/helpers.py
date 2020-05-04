import discord
changed_names = dict()


async def set_prefix(member: discord.Member, prefix):
    changed_names[member.id] = member.display_name
    await member.edit(nick=f'[{prefix}] {member.display_name}'[:32])  # 32 is the discord name limit


async def remove_prefix(member):
    if member.id not in changed_names:
        return
    await member.edit(nick=changed_names.pop(member.id))
