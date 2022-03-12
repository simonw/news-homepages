import csv
import click
import subprocess


HANDLE_LIST = csv.DictReader(open("./sources.csv", "r"))
HANDLE_LOOKUP = dict((d['handle'], d['url']) for d in HANDLE_LIST)


@click.command()
@click.argument('handle')
def main(handle):
    url = HANDLE_LOOKUP[handle]
    subprocess.run([
        "shot-scraper",
        url,
        "-o",
         f"{handle}.jpg",
        "--quality",
        "80",
        "--width",
        "1600",
        "--height",
        "1600",
        "--wait",
        "2000",
    ])


if __name__ == "__main__":
    main()
