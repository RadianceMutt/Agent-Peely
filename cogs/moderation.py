import colorama
import json
import discord
import os
from discord.ext import commands
from discord import slash_command
from discord import Embed, Member
from objects import handling

warnings = {}
mutes = {}
bans = {}

class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    @slash_command(description="Unmutes a member.")
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: Member, reason: str):
        try:
            guild = ctx.guild
            mutedRole = discord.utils.get(guild.roles, name="Muted")

            if not mutedRole:
                mutedRole = await guild.create_role(name="Muted")

                for channel in guild.channels:
                    await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)

            embed = Embed(title="Moderation Action", description=f"Unmuted **{member.name}#{member.discriminator}** ({member.id})")
            embed.add_field(name="Reason", value=f"{reason}", inline=False)
            embed.set_thumbnail(url=member.avatar.url)
            embed.set_author(name=f"Moderator: {ctx.author.name}#{ctx.author.discriminator}", url=ctx.author.avatar.url)

            await member.remove_roles(mutedRole)
            await ctx.respond(embeds=[embed])

        except Exception as error:
            await handling.throw_error(error=error, ctx=ctx)

    @slash_command(description="Mutes a member.")
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: Member, reason: str):
        try:
            guild = ctx.guild
            mutedRole = discord.utils.get(guild.roles, name="Muted")

            if not mutedRole:
                mutedRole = await guild.create_role(name="Muted")

                for channel in guild.channels:
                    await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)

            embed = Embed(title="Moderation Action", description=f"Unmuted **{member.name}#{member.discriminator}** ({member.id})")
            embed.add_field(name="Reason", value=f"{reason}", inline=False)
            embed.set_thumbnail(url=member.avatar.url)
            embed.set_author(name=f"Moderator: {ctx.author.name}#{ctx.author.discriminator}", url=ctx.author.avatar.url)

            await member.add_roles(mutedRole)
            await ctx.respond(embeds=[embed])

        except Exception as error:
            await handling.throw_error(error=error, ctx=ctx)

    @slash_command(description="Kicks a member.")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: Member, reason: str):
        try:
            guild = ctx.guild
            embed = Embed(title="Moderation Action",
                          description=f"Kicked **{member.name}#{member.discriminator}** ({member.id}) from {guild.name}.")
            embed.add_field(name="Reason", value=f"{reason}", inline=False)
            embed.set_thumbnail(url=member.default_avatar.url)
            embed.set_author(name=f"Moderator: {ctx.author.name}#{ctx.author.discriminator}", url=ctx.author.default_avatar.url)

            await member.kick(reason=reason)
            await ctx.respond(embeds=[embed])

        except Exception as error:
            await handling.throw_error(error=error, ctx=ctx)

    @slash_command(description="Bans a member.")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: Member, reason: str):
        try:
            guild = ctx.guild

            embed = Embed(title="Moderation Action", description=f"Banned **{member.name}#{member.discriminator}** ({member.id}) from {guild.name} permanently.")
            embed.add_field(name="Reason", value=f"{reason}", inline=False)
            embed.set_thumbnail(url=member.avatar.url)
            embed.set_author(name=f"Moderator: {ctx.author.name}#{ctx.author.discriminator}", url=ctx.author.avatar.url)

            await member.ban(delete_message_days=7, reason=reason)
            await ctx.respond(embeds=[embed])

        except Exception as error:
            await handling.throw_error(error=error, ctx=ctx)

    @slash_command(description="Warns a member.")
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, member: Member, reason: str):
        try:
            guild = ctx.guild
            embed = Embed(title="Moderation Action", description=f"{member.name} has been warned.")
            embed.add_field(name="Reason", value=f"{reason}")
            embed.set_thumbnail(url=member.avatar.url)
            embed.set_author(name=f"Moderator: {ctx.author.name}#{ctx.author.discriminator}", url=ctx.author.avatar.url)

            dm_embed = Embed(title="Server Infraction", description=f"You have received a warning in {guild.name}.")
            dm_embed.add_field(name="Reason", value=f"{reason}", inline=False)
            dm_embed.add_field(name="Moderator", value=f"{ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})",
                             inline=False)
            dm_embed.add_field(name="Unjust Warning?",
                             value="If you feel like this warning was unjust, you can appeal in the ticket channel.")

            if guild:
                if member in warnings:
                    warnings[member.id].append(reason)
                else:
                    warnings[member.id] = [reason], [warningId] = os.urandom(10)

                with open(r'C:\Users\SIMPL\Documents\MasterTom\data\admin\warns.json', 'w') as f:
                    json.dump(warnings, f)

                await ctx.respond(embeds=[embed])

                await member.create_dm(embeds=[dm_embed])

        except Exception as error:
            await handling.throw_error(error=error, ctx=ctx)


        @slash_command(description="Removes an existing warning from a member.")
        @commands.has_permissions(manage_messages=True)
        async def del_warn(self, ctx, member: Member, warning_id: bytes, reason: str):
            try:
                guild = ctx.guild
                embed = Embed(title="Moderation Action", description=f"Warning `{warning_id}` has been removed for {member.name}.")
                embed.add_field(name="Reason", value=f"{reason}")
                embed.set_thumbnail(url=member.avatar.url)
                embed.set_author(name=f"Moderator: {ctx.author.name}#{ctx.author.discriminator}",
                                 url=ctx.author.avatar.url)

                if guild:
                    if member in warnings:
                        warnings[member.id].remove(reason)
                    else:
                        warnings[member.id] = [reason], [warningId] = os.urandom(10)

                        with open(r'C:\Users\SIMPL\Documents\MasterTom\data\admin\warns.json', 'w') as f:
                            json.dump(warnings, f)

                        await ctx.respond(embeds=[embed])

            except Exception as error:
                await handling.throw_error(error=error, ctx=ctx)

def setup(client):
    client.add_cog(Moderation(client))
    print(colorama.Fore.GREEN + f'[LOG]: {__name__} has loaded.')