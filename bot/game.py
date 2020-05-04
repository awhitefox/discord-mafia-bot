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
            raise ValueError('Game is already running')

        self.voice_channel = voice_c
        self.players.extend(filter(lambda x: not (x.bot or x == master),
                                   self.voice_channel.members))

        # Shuffle players and put master on first place
        random.shuffle(self.players)
        self.players.insert(0, master)

        # Disallow @everyone to speak in current channel
        await self.voice_channel.set_permissions(self.guild.default_role, speak=False)
        # Create role for player and allow them to speak
        self.player_role = await self.guild.create_role(name='Игрок')
        await self.voice_channel.set_permissions(self.player_role, speak=True)
        for p in self.players:
            await p.add_roles(self.player_role)

    async def finish_game(self):
        if not self.is_running():
            raise ValueError('Game is not running')

        # Allow @everybody to speak and delete current_role
        await self.voice_channel.set_permissions(self.guild.default_role, speak=None)
        await self.player_role.delete()

        self.voice_channel = None
        self.player_role = None
        self.players.clear()

    def get_prefix(self, member):
        if member in self.players:
            i = self.players.index(member)
            return f'{self.players.index(member):02d}' if i != 0 else 'В'
        else:
            return 'Н'
