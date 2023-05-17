import json
import os
import random
import discord
import colorama
from discord.ext import commands
from discord import slash_command
from discord import Embed
from discord.ui import InputText, Modal
from os import urandom
from objects import handling
from config import anon_names

links = {}

class BugReportModal(Modal):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(
            InputText(label="Report Title", placeholder="Put a title of your bug report here.", style=discord.InputTextStyle.singleline),
            InputText(label="Bug Description", placeholder="Please always include the traceback if you get an error.", style=discord.InputTextStyle.long),
            InputText(label="Name", placeholder="Leave this field empty if you want to stay anonymous.", style=discord.InputTextStyle.singleline),
            *args, **kwargs
        )

        async def callback(self, interaction: discord.Interaction):
            embed = discord.Embed(title="Bug Report", description="Your bug report has been submitted.")
            embed.add_field(name="Title", value=self.children[0].value, inline=False)
            embed.add_field(name="Description", value=self.children[1].value, inline=False)
            embed.add_field(name="Your Name", value=self.children[2].value, inline=False)

            embed.set_author(name=f"Report Number: {urandom(10)}")

            if self.children[2].value is None:
                embed.set_field_at(index=2, name="Your Name", value=f"Anonymous {random.choice(anon_names)}")

            await interaction.response.send_message(embeds=[embed], ephemeral=True)


class BugReportView(discord.ui.Button):
    @discord.ui.button(label="Report Bug", style=discord.ButtonStyle.primary, emoji="📨")
    async def button_callback(self, button, interaction):
        modal = BugReportModal(title="Report a bug")
        await interaction.response.send_modal(modal)

class Utility(commands.Cog):

    def __init__(self, client):
        self.client = client

    @slash_command(description="Got an traceback or a feature that's not working, create a bug report ticket.")
    async def bug_report(self, ctx: discord.ApplicationContext):
        modal = BugReportModal(title="Report a bug")
        await ctx.send_modal(modal)
        await modal.callback(interaction=discord.InteractionType.modal_submit)

    @slash_command(description="Adds a new link to the blacklist or whitelist.")
    @commands.has_permissions(manage_messages=True)
    async def add_link(self, ctx, link: str, is_blacklist: bool, is_whitelist: bool):
        try:
            if is_blacklist == True:
                embed = Embed(title="Blacklist Update",
                              description=f"The link `{link}` has been added to the blacklist. 👍")
                embed.set_footer(text="All data is saved to JSON as the developer is used to working with JSON data.")

                if ctx.guild:
                    if link in links:
                        link[random.randint(1, 999999)].append(link)
                    else:
                        link[random.randint(1, 999999)] = [link]

                    with open(r'C:\Users\SIMPL\Documents\MasterTom\data\server\config\blacklist\links.json', 'w') as f:
                        json.dump(link, f)

                    await ctx.respond(embeds=[embed])

            elif is_whitelist == True:
                embed = Embed(title="Whitelist Update",
                              description=f"The link `{link}` has been added to the whitelist. 👍")
                embed.set_footer(text="All data is saved to JSON as the developer is used to working with JSON data.")

                if ctx.guild:
                    if link in links:
                        link[random.randint(1, 999999)].append(link)
                    else:
                        link[f"0x{os.urandom(10)}"] = [link]

                    with open(r'C:\Users\SIMPL\Documents\MasterTom\data\server\config\whitelist\links.json', 'w') as f:
                        json.dump(link, f)

                    await ctx.respond(ctx.author.mention, embeds=[embed])

        except Exception as error:
            await ctx.respond(embeds=[await handling.throw_error(error=error, ctx=ctx)], view=BugReportView())


    @slash_command(description="Responds with an randomly generated sentence containing your name and pronouns.")
    async def tryout(self, ctx, name: str, subject_pronoun: str,
                     object_pronoun: str, possessive_determiner: str,
                     possessive_pronoun: str, reflexive_pronoun: str):

       try:
           sentences = [f"I am going to visit {name}'s house today as it is {possessive_determiner} birthday!",
                        f"{name.title()} is a very hardworking person. {subject_pronoun.title()} always tries {possessive_determiner} best.",
                        f"I made a fursuit for {name}. Without {object_pronoun}, this suit would not be possible!",
                        f"Hey! Don't steal {name}'s pen! That's {possessive_pronoun}",
                        f"My friend {name} made me this fursuit all by {reflexive_pronoun}",
                        f"{name.title()} has baked cookies for our friend group! {subject_pronoun.title()} is a very good baker!"]

           random_sentence = random.choice(sentences)

           embed = Embed(title="Pronoun Tryout!", description="**This command is incompatible for emojis.**")
           embed.add_field(name="Sentence 1", value=random_sentence)
           embed.set_author(name="For safety reasons, only you can see this message and no one else.")

           await ctx.respond(embeds=[embed], ephemeral=True)

       except Exception as error:
           await ctx.respond(embeds=[handling.throw_error(error=error)], view=BugReportView())

    @slash_command(description="Responds with the Discord API ping!")
    async def ping(self, ctx):
        embed = Embed(title="Discord API Ping", description=f"Pong! 🏓\n```{round(self.client.latency * 1000)}ms```")
        await ctx.respond(embeds=[embed])

def setup(client):
    client.add_cog(Utility(client))
    print(colorama.Fore.GREEN + f'[LOG]: {__name__} has loaded.')