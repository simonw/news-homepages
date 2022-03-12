import csv
from datetime import datetime
import os
import subprocess

import twitter
import click


HANDLE_LIST = csv.DictReader(open("./sources.csv", "r"))
HANDLE_LOOKUP = dict((d['handle'], d['url']) for d in HANDLE_LIST)


@click.command()
@click.argument('handle')
def main(handle):
    # Pull the source’s metadata
    url = HANDLE_LOOKUP[handle]

    # Connect to Twitter
    api = twitter.Api(
        consumer_key=os.getenv('TWITTER_CONSUMER_KEY'),
        consumer_secret=os.getenv('TWITTER_CONSUMER_SECRET'),
        access_token_key=os.getenv('TWITTER_ACCESS_TOKEN_KEY'),
        access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    )

    # Create the headline
    tweet = f"The @{handle} homepage"

    # Get the image
    image_path = f"./{handle}.jpg"
    io = temp_file_read = open(image_path, 'rb')
    media_id = api.UploadMediaSimple(io)

    # Post the media
    api.PostMediaMetadata(media_id, tweet)

    # Make the tweet
    api.PostUpdate(
        tweet,
        media=media_id,
    )


if __name__ == "__main__":
    main()
