# Retweet bot for Twitter, using Python and Tweepy.
# Search query via hashtag or keyword.
# Author: Tyler L. Jones || CyberVox
# Date: Saturday, May 20th - 2017.
# License: MIT License.

import tweepy
from time import sleep
from datetime import datetime
# Import in your Twitter application keys, tokens, and secrets.
# Make sure your keys.py file lives in the same directory as this .py file.
# from keys import *
from os import environ
CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
ACCESS_KEY = environ['ACCESS_KEY']
ACCESS_SECRET = environ['ACCESS_SECRET']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
print('Starting bot : '+dt_string)

validretweet = 0
failedtweet = 0

# Where q='#example', change #example to whatever hashtag or keyword you want to search.
# Where items(5), change 5 to the amount of retweets you want to tweet.
# Make sure you read Twitter's rules on automation - don't spam!
for tweet in tweepy.Cursor(api.search, q='%23radioastronomy%20OR%20%23radioastrophysics%20OR%20%23radioastro').items(50):
    try:
        print('\nRetweet Bot found tweet by @' + tweet.user.screen_name + '. ' + 'Attempting to retweet.')

        tweet.retweet()
        print('Retweet published successfully.')
        validretweet = validretweet + 1

        # Where sleep(10), sleep is measured in seconds.
        # Change 10 to amount of seconds you want to have in-between retweets.
        # Read Twitter's rules on automation. Don't spam!
        sleep(10)

    # Some basic error handling. Will print out why retweet failed, into your terminal.
    except tweepy.TweepError as error:
        print('\nError. Retweet not successful. Reason: ')
        print(error.reason)
        failedtweet = failedtweet + 1

    except StopIteration:
        break

api.update_status (**status** = 'Bot ran at '+dt_string)
print('End bot run. Retweet : '+str(validretweet)+', failed : '+str(failedtweet))
