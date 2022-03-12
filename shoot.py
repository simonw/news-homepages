import csv
import click
import subprocess


HANDLE_LIST = csv.DictReader(open("./sources.csv", "r"))
HANDLE_LOOKUP = dict((d['handle'], d) for d in HANDLE_LIST)

DEFAULT_WIDTH = "1300"
DEFAULT_HEIGHT = "1600"
DEFAULT_WAIT = "2000"


@click.command()
@click.argument('handle')
def main(handle):
    data = HANDLE_LOOKUP[handle]
    subprocess.run([
        "shot-scraper",
        data['url'],
        "-o",
         f"{handle}.jpg",
        "--quality",
        "80",
        "--width",
        data['width'] or DEFAULT_WIDTH,
        "--height",
        data['height'] or DEFAULT_HEIGHT,
        "--wait",
        data['wait'] or DEFAULT_WAIT,
    ])


if __name__ == "__main__":
    main()
