import traceback
from time import time

import discord
from colorama import Fore, Style
from discord.ext import commands

import cogs
import config_vars
from common import Context

intents = discord.Intents.none()
intents.guilds = True
intents.guild_messages = True
intents.guild_reactions = True
intents.message_content = True
intents.dm_messages = True

bot = commands.Bot(
    command_prefix=">",
    allowed_mentions=discord.AllowedMentions(everyone=False, users=False, roles=False),
    intents=intents,
)
# The default help command is removed so a custom one can be added.

# List of names reserved for those who gave cool ideas or reported something interesting.
# please don't spam me asking to be added.  if you send something interesting to me i will add you to the list.
# If your name is in the list and you use the command '>amicool' you'll get a nice message.
cool_names = [
    "nullpxl",
    "Yiggles",
    "JohnHammond",
    "voidUpdate",
    "Michel Ney",
    "theKidOfArcrania",
    "l14ck3r0x01",
    "hasu",
    "KFBI",
    "mrFu",
    "warlock_rootx",
    "d347h4ck",
    "tourpan",
    "careless_finch",
    "fumenoid",
    "_wh1t3r0se_",
    "The_Crazyman",
    "0x0elliot",
]
# This is intended to be circumvented; the idea being that people will change their names to people in this list just so >amicool works for them, and I think that's funny.


@bot.command()
async def prefix(ctx: Context | None, prefix: str):
    """
    Change the command prefix of the bot.

    Parameters
    ----------
    prefix : str
        The new command prefix.
    """
    bot.command_prefix = prefix

    if ctx:
        await ctx.send(f"Prefix set to `{prefix}`!")

    await bot.change_presence(
        activity=discord.Game(name=f"{prefix}help | {prefix}source")
    )


@bot.command()
async def source(ctx: Context):
    """
    Get the source code for this bot.
    """
    await ctx.send(config_vars.SRC_URL)


@bot.command()
async def request(ctx: Context, feature: str):
    """
    Request a feature for the bot.

    If the feature is helpful, your name will be added to the 'cool names' list!

    Parameters
    ----------
    feature : str
        The feature you would like to request.
    """
    # Bot sends a dm to creator with the name of the user and their request.
    creator = await bot.fetch_user(230827776637272064)
    authors_name = str(ctx.author)
    await creator.send(f""":pencil: {authors_name}: {feature}""")
    await ctx.send(f""":pencil: Thanks, "{feature}" has been requested!""")


@bot.command()
async def report(ctx: Context, error_report: str):
    """
    Report an issue with the bot.

    If the issue is helpful, your name will be added to the 'cool names' list!

    Parameters
    ----------
    error_report : str
        The issue you would like to report.
    """
    # Bot sends a dm to creator with the name of the user and their report.
    creator = await bot.fetch_user(230827776637272064)
    authors_name = str(ctx.author)
    await creator.send(f""":triangular_flag_on_post: {authors_name}: {error_report}""")
    await ctx.send(
        f""":triangular_flag_on_post: Thanks for the help, "{
            error_report}" has been reported!"""
    )


@bot.command()
async def amicool(ctx: Context):
    """
    For the truth.
    """
    authors_name = str(ctx.author).split("#")[0]
    if authors_name in cool_names:
        await ctx.send("You are very cool :]")
    else:
        await ctx.send("lolno")
        await ctx.send(
            "Psst, kid.  Want to be cool?  Find an issue and report it or request a feature!"
        )


@bot.command()
@commands.has_permissions(manage_guild=True)
# @commands.is_owner() # Uncomment this line if you want to restrict this command.
async def reload(ctx: Context, extension: str | None = None):
    """
    Reload a cog.

    Parameters
    ----------
    extension : str
        The name of the cog to reload.
    """
    if extension is None:
        for extension in cogs.default:
            try:
                if bot.extensions.get("cogs." + extension):
                    await bot.reload_extension("cogs." + extension)
                    await ctx.send(f"Reloaded {extension}!")
                else:
                    await ctx.send(f"Cog {extension} not loaded, skipping...")
            except Exception as e:
                await ctx.send(f"Failed to reload {extension}: {e}")
        return
    try:
        await bot.reload_extension("cogs." + extension)
        await ctx.send(f"Reloaded {extension}!")
    except Exception as e:
        await ctx.send(f"Failed to reload {extension}: {e}")


@bot.command()
@commands.has_permissions(manage_guild=True)
# @commands.is_owner() # Uncomment this line if you want to restrict this command.
async def unload(ctx: Context, extension: str):
    """
    Unload a cog.

    Parameters
    ----------
    extension : str
        The name of the cog to unload.
    """
    try:
        await bot.unload_extension("cogs." + extension)
        await ctx.send(f"Unloaded {extension}!")
    except Exception as e:
        await ctx.send(f"Failed to unload {extension}: {e}")


@bot.command()
@commands.has_permissions(manage_guild=True)
# @commands.is_owner() # Uncomment this line if you want to restrict this command.
async def load(ctx: Context, extension: str):
    """
    Load a cog.

    Parameters
    ----------
    extension : str
        The name of the cog to load.
    """
    try:
        await bot.load_extension("cogs." + extension)
        await ctx.send(f"Loaded {extension}!")
    except Exception as e:
        await ctx.send(f"Failed to load {extension}: {e}")


@bot.command(description="test command", hidden=True)
async def test(ctx: Context):
    """
    Command to debug the bot.
    """
    await ctx.send("Test command works!")
    print(bot.cogs.keys())
    print([com for com in bot.all_commands.keys() if not bot.all_commands[com].cog])
    print([com for com in bot.all_commands.keys() if bot.all_commands[com].cog])


@bot.event
async def on_ready():
    print(f"{bot.user.name if bot.user else 'Discord Bot'} - Online")
    print(f"discord.py {discord.__version__}\n")

    await prefix.callback(  # pyright: ignore[reportCallIssue]
        None,  # pyright: ignore[reportArgumentType]
        config_vars.DEFAULT_PREFIX,
    )

    success: list[str] = []
    failed: list[str] = []
    for extension in cogs.default:
        try:
            await bot.load_extension("cogs." + extension)
            success.append(extension)
        except Exception as e:
            print(f"Failed to load {extension}: {e}")
            failed.append(extension)

    print(Fore.GREEN, end="")
    print("Loaded cogs: " + ", ".join(success) if success else "None")
    print(Fore.RED, end="")
    print("Failed cogs: " + ", ".join(failed) if failed else "None")
    print(Style.RESET_ALL, end="")
    print("-------------------------------\n")


@bot.event
async def on_command_error(ctx: Context, error: commands.CommandError):
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing a required argument.  Do >help")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send(
            "You do not have the appropriate permissions to run this command."
        )
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send("I don't have sufficient permissions!")
    elif isinstance(error, commands.NoPrivateMessage):
        await ctx.send("This command cannot be used in private messages.")
    else:
        code = hex(int(time()))
        await ctx.send(
            f"An unexpected error occurred. Please contact the bot creator. ID: {code}"
        )
        print(f"[{code}] Uncaught Error: " + str(error))
        traceback.print_exception(type(error), error, error.__traceback__)


@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    await bot.process_commands(message)


if __name__ == "__main__":
    bot.run(config_vars.DISCORD_TOKEN)
