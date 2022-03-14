import csv
from datetime import datetime
import os

import click
import pytz
from telegram import Bot


SOURCE_LIST = list(csv.DictReader(open("./sources.csv", "r")))
SOURCE_LOOKUP = dict((d['handle'], d) for d in SOURCE_LIST)
BUNDLE_LIST = list(csv.DictReader(open("./bundles.csv", "r")))
BUNDLE_LOOKUP = dict((d['slug'], d) for d in BUNDLE_LIST)

TELEGRAM_API_KEY = os.getenv("TELEGRAM_API_KEY")


@click.command()
@click.argument('handle')
def cli(handle):
    """Send a Telegram message for a single source."""
    # Pull the source’s metadata
    data = SOURCE_LOOKUP[handle]

    # Connect to Telegram
    bot = Bot(token=TELEGRAM_API_KEY)

    # Get the timestamp
    now = datetime.now()

    # Convert it to local time
    tz = pytz.timezone(data['timezone'])
    now_local = now.astimezone(tz)

    # Create the caption
    caption = f"The {data['name']} homepage at {now_local.strftime('%-I:%M %p')} local time"

    # Get the image
    image_path = f"./{handle}.jpg"
    io = temp_file_read = open(image_path, 'rb')

    # Make the tweet
    bot.sendPhoto('@newshomepages', io, caption=caption)


if __name__ == "__main__":
    cli()
