from get_tweet import get_tweet
import tweepy
import os
from os import environ
import time

print("Comienza el programa")

CONSUMER_KEY = environ["CONSUMER_KEY"]
CONSUMER_SECRET = environ["CONSUMER_SECRET"]
ACCESS_KEY = environ["ACCESS_KEY"]
ACCESS_SECRET = environ["ACCESS_SECRET"]

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

interval = 60 * 60

while True:
    print('Buscando frase...')        
    tweet = get_tweet()
    api.update_status(tweet)
    print("Tweet enviado!")
    time.sleep(interval)