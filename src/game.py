import discord
import random


class Game:
    def __init__(self, guild: discord.Guild):
        self.guild = guild
        self.voice_channel = None
        self.player_role = None
        self.players = []

    def is_running(self):
        return self.voice_channel is not None

    async def start_game(self, voice_c: discord.VoiceChannel, master):
        if self.is_running():
            raise RuntimeError('Game is already running')

        self.voice_channel = voice_c
        for m in self.voice_channel.members:
            if not m.bot and not m == master:
                self.players.append(Player(m))

        # Shuffle players and put master on first place
        random.shuffle(self.players)
        self.players.insert(0, Player(master))

        # Disallow @everyone to speak in current channel
        await self.voice_channel.set_permissions(self.guild.default_role, speak=False)
        # Create role for player and allow them to speak
        self.player_role = await self.guild.create_role(name='Игрок')
        await self.voice_channel.set_permissions(self.player_role, speak=True)
        for p in self.players:
            await p.member.add_roles(self.player_role)

    async def finish_game(self):
        if not self.is_running():
            raise RuntimeError('Game is not running')

        # Allow @everybody to speak and delete current_role
        await self.voice_channel.set_permissions(self.guild.default_role, speak=None)
        await self.player_role.delete()

        self.voice_channel = None
        self.player_role = None
        self.players.clear()

    def get_prefix(self, member: discord.Member):
        for i in range(len(self.players)):
            if self.players[i].member == member:
                return f'{i:02d}' if i != 0 else 'В'
        return 'Н'


class Player:
    def __init__(self, member: discord.Member):
        self.member = member
