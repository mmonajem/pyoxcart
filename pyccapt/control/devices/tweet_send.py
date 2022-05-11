"""
This is the main script for sending tweets on the tweeter account of the instrument.
"""

import tweepy

# here we define the keys for the tweeter account
consumer_key = 'xxxxxxxxxxxxx'
consumer_secret = 'xxxxxxxxxxxxxxxxxxxxxxxxx'
access_token = 'xxxxxxxxxxxxxxxx-xxxxxxxxxxx'
access_token_secret = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'


def tweet_send(message):
    """
    This functions update status on twitter.

    Attributes:
        message: message to be updated as status in twitter [string]

    Returns:
        Does not return anything.
    """

    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # Create API object
    api = tweepy.API(auth)

    # Create a tweet
    api.update_status(message)
