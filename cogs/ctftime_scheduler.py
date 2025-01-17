from discord.ext import commands, tasks
import discord
from datetime import datetime
import pytz
import os

# Uncomment for troubleshooting
# import logging
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger('CTFTimeScheduler')

class CTFTimeScheduler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.timezone = pytz.timezone('Asia/Kolkata')
        self.weekly_announcement.start()
        # For testing, uncomment below
        # self.bot.loop.create_task(self.test_announcement())
        
    def cog_unload(self):
        self.weekly_announcement.cancel()

    async def _send_announcement(self):
        try:
            channel = self.bot.get_channel(int(os.getenv('ANNOUNCEMENT_CHANNEL_ID')))
            if not channel:
                return
                
            security_role = channel.guild.get_role(int(os.getenv('SECURITY_ROLE_ID')))
            if not security_role:
                return

            ctftime_command = self.bot.get_command('ctftime')
            if not ctftime_command:
                return
                
            temp_message = await channel.send("Initializing CTF announcement...")
            ctx = await self.bot.get_context(temp_message)
            await temp_message.delete()
            
            await channel.send(f"Here are the upcoming CTFs this week {security_role.mention}!")
            
            upcoming_command = ctftime_command.get_command('upcoming')
            if upcoming_command:
                await upcoming_command(ctx, 5)

        except Exception as e:
            print(f"Announcement error: {str(e)}")

    @tasks.loop(minutes=1)
    async def weekly_announcement(self):
        current_time = datetime.now(self.timezone)
        target_time = current_time.replace(hour=15, minute=17, second=0, microsecond=0)
        
        # Send announcement if it's Friday at target time
        if current_time.weekday() == 4 and (
            current_time.hour == target_time.hour and 
            current_time.minute == target_time.minute
        ):
            await self._send_announcement()

    @weekly_announcement.before_loop
    async def before_weekly_announcement(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(CTFTimeScheduler(bot))