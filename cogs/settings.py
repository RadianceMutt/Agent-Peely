import colorama
import random
import secrets
import pymongo
import discord
from discord.ext import commands
from discord import slash_command
from discord import Embed, Member
from objects import handler
from config import client_url


class Settings(commands.Cog):

    def __init__(self, client):
        self.client = client

    @slash_command(name="set-modlog-channel", description="Sets the channel where all moderation logs will be posted.")
    @commands.has_permissions(administrator=True)
    async def set_modlog_channel_command(self, ctx, channel_id: int):
        pass

    @slash_command(name="view-settings", description="View your settings in the server.")
    @commands.has_permissions(administrator=True)
    async def view_settings_command(self, ctx):
        pass

def setup(client):
    client.add_cog(Settings(client))