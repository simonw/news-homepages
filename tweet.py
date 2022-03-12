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
    url = HANDLE_LOOKUP[handle]

    api = twitter.Api(
        consumer_key=os.getenv('TWITTER_CONSUMER_KEY'),
        consumer_secret=os.getenv('TWITTER_CONSUMER_SECRET'),
        access_token_key=os.getenv('TWITTER_ACCESS_TOKEN_KEY'),
        access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    )

    api.PostUpdate(f"The @{handle} homepage", media=[f"./{handle}.jpg"])


if __name__ == "__main__":
    main()
