import logging
from typing import Final

import discord
from discord import app_commands
from discord.ext import commands

FORWARD_MSG_FLAG: Final[int] = 16384


@app_commands.guild_only()
class CheckForwardCog(commands.GroupCog, name="checkforward"):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client
        self.logger = logging.getLogger(f"cogs.{self.__cog_name__}")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        # self.logger.info(f"{message.type}, {message.flags} {message.content}")

        if message.flags.value == FORWARD_MSG_FLAG:
            try:
                await message.delete()
                self.logger.info(
                    f"Deleted forwarded message {message.id} ({message.flags})"
                )
            except discord.Forbidden:
                self.logger.warning(
                    f"Unable to message due to missing permissions {message.id} ({message.flags})"
                )


async def setup(client: commands.Bot) -> None:
    cog: CheckForwardCog = CheckForwardCog(client)
    await client.add_cog(cog)
    cog.logger.info("Cog loaded")
