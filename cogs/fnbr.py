import colorama
import discord
import objects.handler
import config
import fortnite_api

from discord.ext import commands
from discord.commands import SlashCommandGroup

fortnite_token = config.fortnite_token
global_language = config.fortnite_language

api = fortnite_api.FortniteAPI(api_key=fortnite_token)

class FortniteBR(commands.Cog):

    def __init__(self, client):
        self.client = client

    fortnite = SlashCommandGroup("fortnite", "Fortnite commands.")

    cosmetic = fortnite.create_subgroup("cosmetic", "Fortnite cosmetics commands.")
    playlist = fortnite.create_subgroup("playlist", "Fortnite playlist commands.")
    shop = fortnite.create_subgroup("shop", "Fortnite item-shop commands.")

    @fortnite.command(description="Shows the latest Fortnite news for Battle Royale.")
    async def news(self, ctx):
        embed = discord.Embed(colour=config.discord_colour)
        embed.set_image(url=api.news.fetch(language="en-US").br.image)

        await ctx.respond(embeds=[embed])

def setup(client):
    client.add_cog(FortniteBR(client))
    print(colorama.Fore.GREEN + f'[LOG]: {__name__} has loaded.')