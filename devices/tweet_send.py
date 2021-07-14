import tweepy

consumer_key = 'nt2pSZkkAjq1qBoIJnQTjkggm'
consumer_secret = 'lAxNSTghMxH0LW04VkzwooSUdCaBG6p0uesfIXGJGbRD2dPDq7'
access_token = '1390595351992750080-mKClT969gS8pQYPyz5imhrtfGIb63J'
access_token_secret = '7SZgGaD0emedHuIK30xDZPCDFRKvc3ml453iLdknusClR'


def tweet_send(message):
    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # Create API object
    api = tweepy.API(auth)

    # Create a tweet
    api.update_status(message)
