import os
from datetime import datetime
from pathlib import Path

import click
import discord
import pytz

from . import utils

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")


class BotClient(discord.Client):
    """A chat client that posts the provided handle."""

    def __init__(self, data, input_path, *args, **kwargs):
        """Initialize object."""
        super().__init__(*args, **kwargs)
        self.data = data
        self.input_path = input_path

    async def on_ready(self):
        """Run after we connect to Discord."""
        await self.post()
        await self.close()

    async def post(self):
        """Post message to Discord channel."""
        # Get the channel
        channel = self.get_channel(952969204892573827)

        # Get the timestamp
        now = datetime.now()

        # Convert it to local time
        tz = pytz.timezone(self.data["timezone"])
        now_local = now.astimezone(tz)

        # Create the caption
        caption = f"The {self.data['name']} homepage at {now_local.strftime('%-I:%M %p')} local time"

        # Get the image
        image_path = self.input_path / f"{self.data['handle']}.jpg"

        # Make the post
        await channel.send(caption, file=discord.File(image_path))


@click.command()
@click.argument("handle")
@click.option("-i", "--input-dir", "input_dir", default="./")
def cli(handle, input_dir):
    """Send a Discord message for a single source."""
    data = utils.get_site(handle)
    input_path = Path(input_dir)
    input_path.mkdir(parents=True, exist_ok=True)
    c = BotClient(data, input_path)
    c.run(DISCORD_BOT_TOKEN)


if __name__ == "__main__":
    cli()
