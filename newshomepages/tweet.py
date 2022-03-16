import os
from datetime import datetime

import click
import pytz
import twitter
from slugify import slugify

from . import utils


@click.group()
def cli():
    """Send a tweet."""
    pass


@cli.command()
@click.argument("handle")
def single(handle):
    """Tweet a single source."""
    # Pull the source’s metadata
    data = utils.get_site(handle)

    # Connect to Twitter
    api = twitter.Api(
        consumer_key=os.getenv("TWITTER_CONSUMER_KEY"),
        consumer_secret=os.getenv("TWITTER_CONSUMER_SECRET"),
        access_token_key=os.getenv("TWITTER_ACCESS_TOKEN_KEY"),
        access_token_secret=os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
    )

    # Get the timestamp
    now = datetime.now()

    # Convert it to local time
    tz = pytz.timezone(data["timezone"])
    now_local = now.astimezone(tz)

    # Create the headline
    tweet = f"The @{handle} homepage at {now_local.strftime('%-I:%M %p')} local time"

    # Get the image
    image_path = f"./{handle}.jpg"
    io = open(image_path, "rb")
    media_id = api.UploadMediaSimple(io)

    # Post the media
    api.PostMediaMetadata(media_id, tweet)

    # Make the tweet
    api.PostUpdate(tweet, media=media_id)


@cli.command()
@click.argument("slug")
def bundle(slug):
    """Tweet four sources as a single tweet."""
    # Pull the source metadata
    bundle = utils.get_bundle(slug)
    target_list = [h for h in utils.get_site_list() if h["bundle"] == slug]

    # Connect to Twitter
    api = twitter.Api(
        consumer_key=os.getenv("TWITTER_CONSUMER_KEY"),
        consumer_secret=os.getenv("TWITTER_CONSUMER_SECRET"),
        access_token_key=os.getenv("TWITTER_ACCESS_TOKEN_KEY"),
        access_token_secret=os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
    )

    # Get the timestamp
    now = datetime.now()

    # Convert it to local time
    tz = pytz.timezone(bundle["timezone"])
    now_local = now.astimezone(tz)

    # Create the headline
    tweet = f"{bundle['name']} homepages at {now_local.strftime('%-I:%M %p')} in {bundle['location']}\n"

    # Loop through all the targets
    media_list = []
    for i, target in enumerate(target_list):
        # Get the list item
        emoji = utils.numoji(i + 1)
        list_item = f"\n{emoji} @{target['handle']}"

        # Tack it on the tweet
        tweet += list_item

        # Get the image
        image_path = f"./{target['handle']}.jpg"
        io = open(image_path, "rb")
        media_id = api.UploadMediaSimple(io)

        # Get the timestamp
        target_now = datetime.now()

        # Convert it to local time
        tz = pytz.timezone(target["timezone"])
        target_local = now.astimezone(target_now)

        # Add the alt text to the image
        alt_text = f"The @{target['handle']} homepage at {target_local.strftime('%-I:%M %p')} local time"
        api.PostMediaMetadata(media_id, alt_text)

        # Add it to our list
        media_list.append(media_id)

    # Add hashtags
    slug = slugify(bundle["name"], separator="")
    date_str = now_local.strftime("%Y%m%d")
    tweet += f"\n\n#{slug} #{date_str}"

    # Make the tweet
    api.PostUpdate(tweet, media=media_list)


if __name__ == "__main__":
    cli()
