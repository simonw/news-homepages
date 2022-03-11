import os
import twitter
from datetime import datetime


def main():
    api = twitter.Api(
        consumer_key=os.getenv('TWITTER_CONSUMER_KEY'),
        consumer_secret=os.getenv('TWITTER_CONSUMER_SECRET'),
        access_token_key=os.getenv('TWITTER_ACCESS_TOKEN_KEY'),
        access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    )
    api.PostUpdate(f"The @latimes homepage", media=["./latimes-1600x1600.jpg"])


if __name__ == "__main__":
    main()
