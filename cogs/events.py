import random
import json
import discord
import colorama
from discord.ext import commands
from discord import Embed

class Events(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user or message.author.bot:
            return



def setup(client):
    client.add_cog(Events(client))
    print(colorama.Fore.GREEN + f'[LOG]: {__name__} has loaded.')