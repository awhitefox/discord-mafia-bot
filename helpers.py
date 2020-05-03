async def set_prefix(member, prefix):
    await member.edit(nick=f'[{prefix}] {member.display_name}'[:32])  # 32 is the discord name limit


async def remove_prefix(member):
    if member.display_name[0] != '[':
        return
    await member.edit(nick=member.display_name.split('] ', 1)[1])
