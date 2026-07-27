import discord
from discord.ext import commands

class RecruitmentAggregator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        # Add the IDs of recruitment channels in other servers to watch
        self.source_channel_ids = [
            123456789012345678,  # Channel 1
            234567890123456789,  # Channel 2
        ]
        
        # Destination channel ID in your home server where messages get reposted
        self.destination_channel_id = 987654321098765432

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # Ignore messages from the bot itself
        if message.author.id == self.bot.user.id:
            return

        # Check if the message came from one of the target recruitment channels
        if message.channel.id in self.source_channel_ids:
            dest_channel = self.bot.get_channel(self.destination_channel_id)
            if not dest_channel:
                print(f"[Error] Destination channel {self.destination_channel_id} not found.")
                return

            # Option A: Forward original embeds if present
            if message.embeds:
                for embed in message.embeds:
                    await dest_channel.send(
                        content=f"📢 **New recruitment post from {message.guild.name} (`#{message.channel.name}`)**:",
                        embed=embed
                    )

            # Option B: Forward text content / attachments if it's a plain message
            elif message.content or message.attachments:
                header = f"📢 **New message from {message.guild.name} (`#{message.channel.name}`)**\n"
                header += f"**Author:** {message.author.name} ({message.author.id})\n"
                header += "----------------------------------------"
                
                # Send text content
                if message.content:
                    await dest_channel.send(f"{header}\n{message.content}")
                
                # Forward attachments if any exist
                for attachment in message.attachments:
                    await dest_channel.send(attachment.url)

async def setup(bot):
    await bot.add_cog(RecruitmentAggregator(bot))
