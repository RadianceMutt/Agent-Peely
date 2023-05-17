import os
import colorama
import config
from discord.ext import commands

client = commands.Bot(intents=config.configured_intents)


@client.event
async def on_ready():
    print(colorama.Fore.BLUE +
          f"[LOG]: Logged into Discord as {client.user.name}#{client.user.discriminator}!\nVersion: {config.version}\nUser ID: {client.user.id}")


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(config.discord_token)