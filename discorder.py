import csv
from datetime import datetime
import os

import click
import discord
import pytz


SOURCE_LIST = list(csv.DictReader(open("./sources.csv", "r")))
SOURCE_LOOKUP = dict((d['handle'], d) for d in SOURCE_LIST)
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")


class BotClient(discord.Client):
    """A chat client that posts the provided handle."""

    def __init__(self, data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = data

    async def on_ready(self):
        await self.post()
        await self.close()

    async def post(self):
        # Get the channel
        channel = self.get_channel(952969204892573827)

        # Get the timestamp
        now = datetime.now()

        # Convert it to local time
        tz = pytz.timezone(self.data['timezone'])
        now_local = now.astimezone(tz)

        # Create the caption
        caption = f"The {self.data['name']} homepage at {now_local.strftime('%-I:%M %p')} local time"

        # Get the image
        image_path = f"./{self.data['handle']}.jpg"

        # Make the post
        await channel.send(caption, file=discord.File(image_path))


@click.command()
@click.argument('handle')
def cli(handle):
    """Send a Discord message for a single source."""
    data = SOURCE_LOOKUP[handle]
    c = BotClient(data)
    c.run(DISCORD_BOT_TOKEN)


if __name__ == "__main__":
    cli()
