import discord
from discord.ext import commands

class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Set your home server ID here to restrict commands exclusively to your server
        self.home_guild_id = 111222333444555666

    async def cog_check(self, ctx: commands.Context):
        # Prevent any prefix command from working outside your own server
        if ctx.guild is None or ctx.guild.id != self.home_guild_id:
            return False
        return True

    @commands.command(name="ping")
    @commands.has_permissions(administrator=True)
    async def ping(self, ctx: commands.Context):
        """Simple check to verify the bot is responding."""
        await ctx.send(f"🏓 Pong! Latency: {round(self.bot.latency * 1000)}ms")

    @commands.command(name="status")
    @commands.has_permissions(administrator=True)
    async def set_status(self, ctx: commands.Context, *, status_text: str):
        """Update the bot's status silently from your home server."""
        await self.bot.change_presence(
            status=discord.Status.idle,
            activity=discord.Game(name=status_text)
        )
        await ctx.send(f"✅ Updated status to: **{status_text}**")

async def setup(bot):
    await bot.add_cog(AdminCommands(bot))
