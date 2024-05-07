import discord
from discord.ext import commands
import help_info
import config_vars
from time import time
from config_vars import Context


intents = discord.Intents.none()
intents.guilds = True
intents.guild_messages = True
intents.guild_reactions = True
intents.message_content = True
intents.dm_messages = True

bot = commands.Bot(command_prefix=">", allowed_mentions=discord.AllowedMentions(
    everyone=False, users=False, roles=False), intents=intents)
# The default help command is removed so a custom one can be added.
bot.remove_command('help')

# Each extension corresponds to a file within the cogs directory.  Remove from the list to take away the functionality.
extensions = ['ctf', 'configuration',
              'encoding', 'cipher', 'utility', 'ctftime']
# List of names reserved for those who gave cool ideas or reported something interesting.
# please don't spam me asking to be added.  if you send something interesting to me i will add you to the list.
# If your name is in the list and you use the command '>amicool' you'll get a nice message.
cool_names = ['nullpxl', 'Yiggles', 'JohnHammond', 'voidUpdate', 'Michel Ney', 'theKidOfArcrania', 'l14ck3r0x01', 'hasu', 'KFBI',
              'mrFu', 'warlock_rootx', 'd347h4ck', 'tourpan', 'careless_finch', 'fumenoid', '_wh1t3r0se_', 'The_Crazyman', '0x0elliot']
# This is intended to be circumvented; the idea being that people will change their names to people in this list just so >amicool works for them, and I think that's funny.


async def change_prefix(ctx: Context | None, prefix: str):
    bot.command_prefix = prefix

    if ctx:
        await ctx.send(f"Prefix set to `{prefix}`!")

    await bot.change_presence(activity=discord.Game(name=f"{prefix}help | {prefix}source"))
bot.command(name="prefix")(change_prefix)


@bot.event
async def on_ready():
    print(f"{bot.user.name if bot.user else "Discord Bot"} - Online")
    print(f"discord.py {discord.__version__}\n")

    await change_prefix(None, config_vars.DEFAULT_PREFIX)

    for extension in extensions:
        try:
            await bot.load_extension("cogs."+extension)
        except Exception as e:
            print(f"Failed to load {extension}: {e}")

    print("Loaded cogs:", bot.cogs.keys())

    print("-------------------------------")


@bot.command()
async def help(ctx: Context, page: str | None = None):
    # Custom help command.  Each main category is set as a 'page'.
    if page == "ctftime":
        emb = discord.Embed(description=help_info.ctftime_help.format(
            prefix=bot.command_prefix), colour=4387968)
        emb.set_author(name="CTFTime Help")
    elif page == "ctf":
        emb = discord.Embed(description=help_info.ctf_help.format(
            prefix=bot.command_prefix), colour=4387968)
        emb.set_author(name="CTF Help")
    elif page == "config":
        emb = discord.Embed(description=help_info.config_help.format(
            prefix=bot.command_prefix), colour=4387968)
        emb.set_author(name="Configuration Help")
    elif page == "utility":
        emb = discord.Embed(description=help_info.utility_help.format(
            prefix=bot.command_prefix), colour=4387968)
        emb.set_author(name="Utilities Help")

    else:
        emb = discord.Embed(description=help_info.help_page.format(
            prefix=bot.command_prefix), colour=4387968)
        emb.set_author(
            name=f"{bot.user.name if bot.user else "Discord Bot"} Help")

    attach_embed_info(ctx, emb)
    await ctx.channel.send(embed=emb)


def attach_embed_info(
    ctx: Context | None = None, embed: discord.Embed | None = None
):
    if embed and bot.user and bot.user.avatar:
        embed.set_thumbnail(url=f"{bot.user.avatar.url}")
    return embed


@bot.command()
async def source(ctx: Context):
    # Sends the github link of the bot.
    await ctx.send(help_info.src)


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
        code = int(time())
        await ctx.send(f"An unexpected error occurred. Please contact the bot creator. ID: {code}")
        print("[code] Uncaught Error: ")
        print(error)


@bot.command()
async def request(ctx: Context, feature: str):
    # Bot sends a dm to creator with the name of the user and their request.
    creator = await bot.fetch_user(230827776637272064)
    authors_name = str(ctx.author)
    await creator.send(f""":pencil: {authors_name}: {feature}""")
    await ctx.send(f""":pencil: Thanks, "{feature}" has been requested!""")


@bot.command()
async def report(ctx: Context, error_report: str):
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
    authors_name = str(ctx.author).split("#")[0]
    if authors_name in cool_names:
        await ctx.send("You are very cool :]")
    else:
        await ctx.send("lolno")
        await ctx.send(
            "Psst, kid.  Want to be cool?  Find an issue and report it or request a feature!"
        )


@bot.command()
async def test(ctx: Context):
    await ctx.send("Test command works!")
    print(bot.cogs.keys())

if __name__ == "__main__":
    bot.run(config_vars.discord_token)
