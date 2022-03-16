import os
from datetime import datetime

import click
import pytz
from telegram import Bot

from . import utils

TELEGRAM_API_KEY = os.getenv("TELEGRAM_API_KEY")


@click.command()
@click.argument("handle")
def cli(handle):
    """Send a Telegram message for a single source."""
    # Pull the source’s metadata
    data = utils.get_site(handle)

    # Connect to Telegram
    bot = Bot(token=TELEGRAM_API_KEY)

    # Get the timestamp
    now = datetime.now()

    # Convert it to local time
    tz = pytz.timezone(data["timezone"])
    now_local = now.astimezone(tz)

    # Create the caption
    caption = (
        f"The {data['name']} homepage at {now_local.strftime('%-I:%M %p')} local time"
    )

    # Get the image
    image_path = f"./{handle}.jpg"
    io = open(image_path, "rb")

    # Send the photo
    bot.sendPhoto("@newshomepages", io, caption=caption)


if __name__ == "__main__":
    cli()
