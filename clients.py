import praw
from imgurpython import ImgurClient
import twitter
import tweepy
import json

#This script contains the classes used to create instances of the
# Reddit and Imgur clients





class RedditConnection:

    def __init__(self, name):
        self.RedditBot = praw.Reddit(name)  # Specifies bot1 in praw.ini as RedditBot


class ImgurConnection:

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.ImgurClientConnection = ImgurClient(self.client_id,self.client_secret)

class TwitterConnection:
    def __init__(self, consumer_key, consumer_secret, access_token_key, access_token_secret):
        self.consumer_key = [consumer_key]
        self.consumer_secret = [consumer_secret]
        self.access_token_key = [access_token_key]
        self.access_token_secret = [access_token_secret]

        self.TwitterClientConnection = twitter.Api(self.consumer_key[0],
                                                   self.consumer_secret[0],
                                                   self.access_token_key[0],
                                                   self.access_token_secret[0], sleep_on_rate_limit=True)

        self.authentication = tweepy.OAuthHandler(self.consumer_key[0], self.consumer_secret[0])
        self.authentication.set_access_token(self.access_token_key[0], self.access_token_secret[0])
        self.TweepyAPIConnection = tweepy.API(self.authentication)





