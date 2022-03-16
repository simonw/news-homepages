import os
from datetime import datetime

import click
import internetarchive
import pytz

from . import utils

IA_ACCESS_KEY = os.getenv("IA_ACCESS_KEY")
IA_SECRET_KEY = os.getenv("IA_SECRET_KEY")
IA_COLLECTION = os.getenv("IA_COLLECTION")


@click.command()
@click.argument("handle")
def cli(handle):
    """Archive a screenshot."""
    # Pull the source’s metadata
    data = utils.get_site(handle)

    # Get the timestamp
    now = datetime.now()

    # Convert it to local time
    tz = pytz.timezone(data["timezone"])
    now_local = now.astimezone(tz)

    title = (
        f"The @{data['url']} homepage at {now_local.strftime('%-I:%M %p')} local time"
    )

    identifier = f"{handle}-{now_local.strftime('%s')}"
    kwargs = dict(
        files=[open(f"./{handle}.jpg", "rb")],
        metadata=dict(
            title=title,
            collection=IA_COLLECTION,
            mediatype="image",
            publisher=data["url"],
            date=str(now_local),
            contributor="https://github.com/palewire/news-homepages",
        ),
        access_key=IA_ACCESS_KEY,
        secret_key=IA_SECRET_KEY,
    )
    internetarchive.upload(identifier, **kwargs)


if __name__ == "__main__":
    cli()
