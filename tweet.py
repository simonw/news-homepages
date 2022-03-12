import csv
from datetime import datetime
import os
import subprocess

import click
import pytz
import twitter


HANDLE_LIST = csv.DictReader(open("./sources.csv", "r"))
HANDLE_LOOKUP = dict((d['handle'], d) for d in HANDLE_LIST)


@click.command()
@click.argument('handle')
def main(handle):
    # Pull the source’s metadata
    data = HANDLE_LOOKUP[handle]

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


if __name__ == "__main__":
    main()
