from discord import Embed

async def throw_error(error, ctx):
    embed = Embed(title="An error has occurred!", description="Don't worry. It's not your fault.")
    embed.add_field(name="Traceback", value=f"```{error}```", inline=False)
    embed.add_field(name="Bug Report", value="You can submit a bug report by either running `/bug_report` or clicking the button below.", inline=False)

    embed.set_footer(text="I am in beta development and is bound to have bugs and issues.")

    await ctx.respond(embeds=[embed])