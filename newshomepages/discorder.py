import os
import typing
from datetime import datetime
from pathlib import Path

import click
import discord
import pytz

from . import utils

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")


class BotClient(discord.Client):
    """A chat client that posts the provided handle."""

    def __init__(self, data: dict, input_path: Path, *args, **kwargs):
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
        image_path = self.input_path / f"{self.data['handle'].lower()}.jpg"

        # Make the post
        await channel.send(caption, file=discord.File(image_path))


@click.group()
def cli():
    """Send a Discord message."""
    pass


@cli.command()
@click.argument("handle")
@click.option("-i", "--input-dir", "input_dir", default="./")
def single(handle: str, input_dir: str):
    """Send a single source."""
    site = utils.get_site(handle)
    _post(site, input_dir)


@cli.command()
@click.argument("slug")
@click.option("-i", "--input-dir", "input_dir", default="./")
def bundle(slug: str, input_dir: str):
    """Send a bundle of sources."""
    site_list = utils.get_sites_in_bundle(slug)
    for site in site_list:
        _post(site, input_dir)


async def _post(site: typing.Dict, input_dir: str):
    input_path = Path(input_dir)
    c = BotClient(site, input_path)
    c.run(DISCORD_BOT_TOKEN)
    await c.close()


if __name__ == "__main__":
    cli()
