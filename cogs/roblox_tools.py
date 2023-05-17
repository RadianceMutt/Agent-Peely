from requests import get
from discord.ext import commands
from discord import slash_command
from discord import Embed
from roblox import Client, AvatarThumbnailType
from objects import handling
import colorama

init = Client()


class Roblox(commands.Cog):

    def __init__(self, client):
        self.client = client

    @slash_command(description="Displays information about a Roblox accessory.")
    async def display_roblox_item(self, ctx, item_id: int):
        pass

    @slash_command(description="Displays information about a Roblox group.")
    async def display_roblox_group(self, ctx, group_id: int):
        try:
            group = await init.get_group(group_id=group_id)
            icons = await init.thumbnails.get_group_icons(
                groups=[group],
                size=(420, 420)
            )
            embed = Embed(title=f"{group.name} - Group Information", url=f"https://www.roblox.com/groups/{group_id}")

            embed.add_field(name="Owner",
                            value=f"[{group.owner.name} / @{group.owner.display_name}](https://www.roblox.com/users/{group.owner.id}/profile)",
                            inline=False)
            embed.add_field(name="ID", value=f"{group.id}", inline=True)
            embed.add_field(name="Member Count", value=f"{group.member_count: ,}", inline=False)
            embed.add_field(name="Description", value=group.description, inline=False)

            if group.is_locked is True:
                embed.set_author(name="This group has been locked! 💀")

            if group.public_entry_allowed is False:
                embed.set_author(name="This group is private! 🔒")
            else:
                embed.set_author(name="This group is free to enter! 🔓")

            if len(icons) > 0:
                icon = icons[0]
                embed.set_thumbnail(url=icon.image_url)

            if group.description is None:
                embed.set_field_at(index=3, name="Description", value="This group has no description filled in!",
                                   inline=False)

            await ctx.respond(embeds=[embed])

        except Exception as error:
            await handling.throw_error(error=error, ctx=ctx)

    @slash_command(description="Displays data about a Roblox player.")
    async def display_roblox_player(self, ctx, user_id: int):
        player = await init.get_user(user_id=user_id)
        followers = await player.get_follower_count()
        followings = await player.get_following_count()
        friends = await player.get_friend_count()

        response = get(url=f"https://users.roblox.com/v1/users/{user_id}").json()
        full_body = await init.thumbnails.get_user_avatar_thumbnails(
            users=[player],
            type=AvatarThumbnailType.full_body,
            size=(420, 420)
        )
        headshot = await init.thumbnails.get_user_avatar_thumbnails(
            users=[player],
            type=AvatarThumbnailType.headshot,
            size=(420, 420)
        )

        embed = Embed(title=f"{player.display_name}'s Profile", url=f"https://roblox.com/users/{user_id}/profile")
        embed.add_field(name="Description", value=f"{player.description}", inline=False)
        embed.add_field(name="Name", value=f"@{player.name}", inline=True)
        embed.add_field(name="Join Date", value=player.created.strftime('%d/%m/%Y, %H:%M:%S'), inline=False)
        embed.add_field(name="Followers", value=f"{followers: ,}", inline=False)
        embed.add_field(name="Following", value=f"{followings: ,}", inline=False)
        embed.add_field(name="Friend Count", value=f"{friends: ,}", inline=False)

        if len(headshot) > 0:
            thumbnail = headshot[0]
            embed.set_thumbnail(url=thumbnail.image_url)

        if len(headshot) > 0:
            thumbnail = full_body[0]
            embed.set_image(url=thumbnail.image_url)

        if response['hasVerifiedBadge'] is True:
            embed.set_author(name="This player is verified! ✅")
        else:
            if player.is_banned is True:
                embed.set_author(name="This player is banned! ❌")

        await ctx.respond(embeds=[embed])


def setup(client):
    client.add_cog(Roblox(client))
    print(colorama.Fore.GREEN + f'[LOG]: {__name__} has loaded.')
