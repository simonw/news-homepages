import csv
from datetime import datetime
import os
import subprocess

import click
import pytz
from slugify import slugify
import twitter


SOURCE_LIST = list(csv.DictReader(open("./sources.csv", "r")))
SOURCE_LOOKUP = dict((d['handle'], d) for d in SOURCE_LIST)
BUNDLE_LIST = list(csv.DictReader(open("./bundles.csv", "r")))
BUNDLE_LOOKUP = dict((d['slug'], d) for d in BUNDLE_LIST)


@click.group()
def cli():
    pass


@cli.command()
@click.argument('handle')
def single(handle):
    """Tweet a single source."""
    # Pull the source’s metadata
    data = SOURCE_LOOKUP[handle]

    # Connect to Twitter
    api = twitter.Api(
        consumer_key=os.getenv('TWITTER_CONSUMER_KEY'),
        consumer_secret=os.getenv('TWITTER_CONSUMER_SECRET'),
        access_token_key=os.getenv('TWITTER_ACCESS_TOKEN_KEY'),
        access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    )

    # Get the timestamp
    now = datetime.now()

    # Convert it to local time
    tz = pytz.timezone(data['timezone'])
    now_local = now.astimezone(tz)

    # Create the headline
    tweet = f"The @{handle} homepage at {now_local.strftime('%-I:%M %p')} local time"

    # Get the image
    image_path = f"./{handle}.jpg"
    io = temp_file_read = open(image_path, 'rb')
    media_id = api.UploadMediaSimple(io)

    # Post the media
    api.PostMediaMetadata(media_id, tweet)

    # Make the tweet
    api.PostUpdate(tweet, media=media_id)


@cli.command()
@click.argument('slug')
def bundle(slug):
    """Tweet four sources as a single tweet."""
    # Pull the source metadata
    bundle = BUNDLE_LOOKUP[slug]
    target_list = [h for h in SOURCE_LIST if h['bundle'] == slug]

    # Connect to Twitter
    api = twitter.Api(
        consumer_key=os.getenv('TWITTER_CONSUMER_KEY'),
        consumer_secret=os.getenv('TWITTER_CONSUMER_SECRET'),
        access_token_key=os.getenv('TWITTER_ACCESS_TOKEN_KEY'),
        access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    )

    # Get the timestamp
    now = datetime.now()

    # Convert it to local time
    tz = pytz.timezone(bundle['timezone'])
    now_local = now.astimezone(tz)

    # Create the headline
    tweet = f"{bundle['name']} homepages at {now_local.strftime('%-I:%M %p')} in {bundle['location']}\n"

    # Loop through all the targets
    media_list = []
    for i, target in enumerate(target_list):
        # Get the list item
        emoji = numoji(i+1)
        list_item = f"\n{emoji} @{target['handle']}"

        # Tack it on the tweet
        tweet += list_item

        # Get the image
        image_path = f"./{target['handle']}.jpg"
        io = temp_file_read = open(image_path, 'rb')
        media_id = api.UploadMediaSimple(io)

        # Get the timestamp
        target_now = datetime.now()

        # Convert it to local time
        tz = pytz.timezone(target['timezone'])
        target_local = now.astimezone(target_now)

        # Add the alt text to the image
        alt_text = f"The @{target['handle']} homepage at {target_local.strftime('%-I:%M %p')} local time"
        api.PostMediaMetadata(media_id, alt_text)

        # Add it to our list
        media_list.append(media_id)

    # Add hashtags
    slug = slugify(bundle['name'], separator='')
    date_str = now_local.strftime("%Y%m%d")
    tweet += f"\n\n#{slug} #{date_str}"

    # Make the tweet
    api.PostUpdate(tweet, media=media_list)


def numoji(number):
    """Convert a number into a series of emojis for Slack.

    Args:
        number (int): The number to convert into emoji

    Returns: Am emoji string
    """
    # Convert the provided number to a string
    s = str(number)

    # Split it into a list of tokens, one per number
    parts = list(s)

    # Create crosswalk between numerals and emojis
    lookup = {
        '0': "0️⃣",
        '1': "1️⃣",
        '2': "2️⃣",
        '3': "3️⃣",
        '4': "4️⃣",
        '5': "5️⃣",
        '6': "6️⃣",
        '7': "7️⃣",
        '8': "8️⃣",
        '9': "9️⃣",
    }

    # Look up each of the tokens in the crosswalk
    emojis = list(map(lookup.get, parts))

    # Join it all together and return the result
    return "".join(emojis)


if __name__ == "__main__":
    cli()
