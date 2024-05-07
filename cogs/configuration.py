import config_vars
import discord
from discord.ext import commands
from config_vars import Context

# Extension for per-discord-server configuration.
# Configurations are logged in the database under the server id (right click on your server icon in discord dev mode).


class Configuration(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.group()
    async def config(self, ctx: Context):
        if ctx.invoked_subcommand is None:
            # If the subcommand passed does not exist, its type is None
            config_commands = list(
                set([c.qualified_name for c in Configuration.walk_commands(self)][1:])
            )
            await ctx.send(f"Current config commands are: {', '.join(config_commands)}")

    @commands.bot_has_permissions(manage_channels=True)
    @commands.has_permissions(manage_channels=True)
    @commands.guild_only()
    @config.command()
    async def ctf_category(self, ctx: Context, category_name: str):
        # Set the category that new ctf channels are created in by default.
        category_name = category_name.replace("$", "")
        if ctx.guild is None:
            raise commands.NoPrivateMessage

        category = discord.utils.get(ctx.guild.categories, name=category_name)

        if (
            category == None
        ):  # Checks if category exists, if it doesn't it will create it.
            await ctx.guild.create_category(name=category_name)
            category = discord.utils.get(
                ctx.guild.categories, name=category_name)

        sconf = config_vars.serverdb[
            str(ctx.guild.id) + "-CONF"
        ]  # sconf means server configuration
        info = {"ctf_category": category_name}
        sconf.update_one({"name": "category_name"}, {
                         "$set": info}, upsert=True)
        categoryset = sconf.find_one({"name": "category_name"})
        if categoryset is None:
            raise ValueError("CTF category not set")
        await ctx.send(f"CTF category set as `{categoryset["ctf_category"]}`")

    @commands.bot_has_permissions(manage_channels=True)
    @commands.has_permissions(manage_channels=True)
    @commands.guild_only()
    @config.command()
    async def archive_category(self, ctx: Context, category_name: str):
        category_name = category_name.replace("$", "")
        if ctx.guild is None:
            raise commands.NoPrivateMessage

        # Set the category that archived ctf channels are put in by default.
        category_name = category_name.replace("$", "")
        category = discord.utils.get(ctx.guild.categories, name=category_name)

        if (
            category == None
        ):  # Checks if category exists, if it doesn't it will create it.
            await ctx.guild.create_category(name=category_name)
            category = discord.utils.get(
                ctx.guild.categories, name=category_name)

        sconf = config_vars.serverdb[
            str(ctx.guild.id) + "-CONF"
        ]  # sconf means server configuration
        info = {"archive_category": category_name}
        sconf.update_one({"name": "archive_category_name"},
                         {"$set": info}, upsert=True)
        categoryset = sconf.find_one({"name": "archive_category_name"})
        if categoryset is None:
            raise ValueError("Archive category not set")
        await ctx.send(f"Archive category set as `{categoryset["archive_category"]}`")


async def setup(bot: commands.Bot):
    await bot.add_cog(Configuration(bot))
