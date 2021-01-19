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
retweetdone = 0
failedtweet = 0
waittime = 90 # in seconds

# Where q='#example', change #example to whatever hashtag or keyword you want to search.
# Where items(5), change 5 to the amount of retweets you want to tweet.
# Make sure you read Twitter's rules on automation - don't spam!

# RUN ROUNDS - 1 : RADIO ASTRONOMY

keydict = {
    'radio astronomy' : ['radio astro','radio-astro','radioastro','radio sun','radio galax','active galax'],
    'radio telescope' : ['radioastro','lofar','gmrt','vla','vlbi','nrao','ska']
}

searchkeys = keydict.keys()
for key in searchkeys:
    print('Searched for',key)
    search_results = api.search(q=key, count=50,tweet_mode='extended')
    mandatory_keywords = keydict[key]
    goodtweet = (fulltweet for fulltweet in search_results for goodkeys in mandatory_keywords if goodkeys in fulltweet.full_text.lower())
    cc = 0
    for tweet in goodtweet:
        if (not tweet.retweeted) and ('rt @' not in tweet.full_text.lower()) and (not tweet.in_reply_to_status_id) and (not tweet.user.screen_name.lower() == 'astronomyradio'):
            validretweet = validretweet + 1
            try:
                tweet.retweet()
                retweetdone = retweetdone + 1
                print('SUCCESSFULL @' + tweet.user.screen_name)

                # Where sleep(10), sleep is measured in seconds.
                # Change 10 to amount of seconds you want to have in-between retweets.
                # Read Twitter's rules on automation. Don't spam!
                sleep(waittime)

            # Some basic error handling. Will print out why retweet failed, into your terminal.
            except tweepy.TweepError as error:
                print('FAILED : @' + tweet.user.screen_name + ' : '+error.reason)
                failedtweet = failedtweet + 1

            except StopIteration:
                break

print('\nEnd bot run. Valid tweets : '+str(validretweet)+', successful : '+str(retweetdone)+' failed : '+str(failedtweet))
