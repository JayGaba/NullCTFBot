import collections
import string
from discord.ext import commands
from config_vars import Context


class Ciphers(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def rot(self, ctx: Context, message: str):
        # Bruteforce a rot cipher.
        allrot = ""

        for i in range(0, 26):
            upper = collections.deque(string.ascii_uppercase)
            lower = collections.deque(string.ascii_lowercase)

            upper.rotate((-i))
            lower.rotate((-i))

            upper = "".join(list(upper))
            lower = "".join(list(lower))
            translated = message.translate(
                str.maketrans(string.ascii_uppercase, upper)
            ).translate(str.maketrans(string.ascii_lowercase, lower))
            allrot += "{}: {}\n".format(i, translated)

        await ctx.send(f"```{allrot}```")

    @commands.command()
    async def atbash(self, ctx: Context, message: str):
        # Return the result of performing the atbash cipher on the message.
        normal = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        changed = "zyxwvutsrqponmlkjihgfedcbaZYXWVUTSRQPONMLKJIHGFEDCBA"
        trans = str.maketrans(normal, changed)
        atbashed = message.translate(trans)
        await ctx.send(atbashed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Ciphers(bot))
