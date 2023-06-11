import random
import requests
import e621
import colorama
from discord.ext import commands
from discord import SlashCommandGroup
from discord import Embed

import config
from objects import handler

api = e621.api
endpoints = api.endpoints

class Images(commands.Cog):

    def __init__(self, client):
        self.client = client

    images = SlashCommandGroup("images", "Image commands.")

    fortnite = images.create_subgroup("fortnite", "Fortnite image commands.")
    furry = images.create_subgroup("furry", "Furry image commands.")

    @furry.command(description="Searches for furry images on e621.net.")
    @commands.cooldown(1, 5, commands.BucketType.default)
    async def search(self, ctx, query: str, is_nsfw: bool):
        try:
            if is_nsfw == True:
                await ctx.respond("Please use the `is_nsfw` parameter when executing this command in a NSFW channel.", ephemeral=True)
            else:
                page = random.randint(1, 999)
                posts_endpoint = endpoints.Posts
                search = posts_endpoint.search(self=self, tags=query, ignore_pagination=True)

                for post in search:
                    url = post.file_url

                    if post.rating == "Explicit" or "Questionable" and is_nsfw == False:
                        await ctx.respond("The post I found was NSFW! Either try again in a NSFW channel or rerun the command.", ephemeral=True)
                    else:

                        embed = Embed(title="100% Furry Trash 🐾", colour=config.discord_colour)

                        embed.set_author(name=f"Original Artist: {post.tag_string_artist.title()}")
                        embed.set_image(url=url)
                        embed.add_field(name="Original Source", value=f"[Click here to go to the source image.]({post.sources[1]})")

                        await ctx.respond(embeds=[embed])

        except Exception as error:
            await handler.throw_error(error=error, ctx=ctx)

    @furry.command(description="Sends a randomly picked sfw image of a furry!")
    @commands.cooldown(1, 5, commands.BucketType.default)
    async def sfw(self, ctx):
        try:
            response = requests.get(url="http://sheri.bot/api/mur/").json()
            embed = Embed(title=f"Here you go, {ctx.author.name}!", url=response['source'], colour=config.discord_colour)

            embed.add_field(name="Inappropriate Image?",
                            value=f"[Report it here by clicking this link.]({response['report_url']})")
            embed.set_author(name=f"Original Artist: {response['author']['name']}", url=response['author']['link'])
            embed.set_image(url=response['url'])

            embed.set_footer(text="Powered by Sheri API!")

            await ctx.respond(embeds=[embed])

        except Exception as error:
            await handler.throw_error(error=error, ctx=ctx)


def setup(client):
    client.add_cog(Images(client))
    print(colorama.Fore.GREEN + f'[LOG]: {__name__} has loaded.')