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

db_client = pymongo.MongoClient(client_url)
print(colorama.Fore.GREEN + f"[LOG]: Successfully connected to MongoDB cluster 1 for {__name__}.")

db = db_client.moderation

moderation = discord.SlashCommandGroup("moderation", "Moderative commands.")

class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    @moderation.command(description="Unmutes a member.")
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(1, 20, commands.BucketType.default)
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
            await handler.throw_error(error=error, ctx=ctx)

    @moderation.command(description="Mutes a member.")
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(1, 20, commands.BucketType.default)
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
            await handler.throw_error(error=error, ctx=ctx)

    @moderation.command(description="Kicks a member.")
    @commands.has_permissions(kick_members=True)
    @commands.cooldown(1, 20, commands.BucketType.default)
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
            await handler.throw_error(error=error, ctx=ctx)

    @moderation.command(description="Bans a member.")
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1, 20, commands.BucketType.default)
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
            await handler.throw_error(error=error, ctx=ctx)

    @moderation.command(description="Warns a member.")
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 20, commands.BucketType.default)
    async def warn(self, ctx, member: Member, reason: str):
        try:

            guild = ctx.guild
            warning_id = secrets.token_hex(16)

            embed = Embed(title="Moderation Action", description=f"{member.name} has been warned.")
            embed.add_field(name="Reason", value=f"{reason}")
            embed.set_thumbnail(url=member.avatar.url)
            embed.set_author(name=f"Moderator: {ctx.author.name}#{ctx.author.discriminator}", url=ctx.author.avatar.url)

            dm_embed = Embed(title="You have received a warning.", description="Repeated offences will lead to a harsher consequences.")
            dm_embed.add_field(name="Reason", value=reason)
            dm_embed.add_field(name="Moderator", value=f"{ctx.author.name}#{ctx.author.discriminator}")

            embed.set_thumbnail(url=member.avatar.url)


            db.warning_logs.insert_one(
                {
                    f"{ctx.guild.id}": {
                        "warnings": {
                            f"{warning_id}": {
                                "user-id": member.id,
                                "reason": reason,
                                "moderator": ctx.author.id
                            }
                        }
                    }
                }
            )

            await ctx.respond(embeds=[embed])
            await member.send(f"{member.mention}", embeds=[dm_embed])

        except Exception as error:
            await handler.throw_error(error=error, ctx=ctx)


        @moderation.command(description="Removes an existing warning from a member.")
        @commands.has_permissions(manage_messages=True)
        @commands.cooldown(1, 20, commands.BucketType.default)
        async def del_warn(self, ctx, member: Member, warning_id: int, reason: str):
            try:
                guild = ctx.guild
                embed = Embed(title="Moderation Action", description=f"Warning `{warning_id}` has been removed for {member.name}.")
                embed.add_field(name="Reason", value=f"{reason}")
                embed.set_thumbnail(url=member.avatar.url)
                embed.set_author(name=f"Moderator: {ctx.author.name}#{ctx.author.discriminator}",
                                 url=ctx.author.avatar.url)


                await ctx.respond(embeds=[embed])

            except Exception as error:
                await handler.throw_error(error=error, ctx=ctx)

def setup(client):
    client.add_cog(Moderation(client))
    print(colorama.Fore.GREEN + f'[LOG]: {__name__} has loaded.')