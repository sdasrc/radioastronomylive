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
waittime = 80 # in seconds

# Where q='#example', change #example to whatever hashtag or keyword you want to search.
# Where items(5), change 5 to the amount of retweets you want to tweet.
# Make sure you read Twitter's rules on automation - don't spam!

keywords = ['#radioastronomy','#radioastrophysics','#radiotelescope','radio astro','radioastro','radio-astro','lofar','gmrt','vla','vlbi','nrao','ska']
excludename = ['AstronomyRadio']
results = []
for key in keywords:    
    search_results = api.search(q=key, count=50,tweet_mode='extended')
    results = results + search_results
    
for tweet in results:
    fultxt = tweet.full_text
    fultxt = fultxt.lower()
    if (not tweet.retweeted) and ('rt @' not in tweet.full_text) and (not tweet.in_reply_to_status_id) and ('radio' in fultxt) and (not tweet.user.screen_name == 'AstronomyRadio') and ( ('radio astro' in fultxt) or ('lofar' in fultxt) or ('gmrt' in fultxt) or ('nrao' in fultxt)  or ('vlbi' in fultxt)  or ('vla' in fultxt) or ('ska' in fultxt) or ('radio-astro' in fultxt) or ('radioastro' in fultxt) or ('radiotelescope' in fultxt) ):
        try:
            validretweet = validretweet + 1
            tweet.retweet()
            retweetdone = retweetdone + 1
            print('Retweet by @' + tweet.user.screen_name + ' published successfully.')

            # Where sleep(10), sleep is measured in seconds.
            # Change 10 to amount of seconds you want to have in-between retweets.
            # Read Twitter's rules on automation. Don't spam!
            sleep(waittime)

        # Some basic error handling. Will print out why retweet failed, into your terminal.
        except tweepy.TweepError as error:
            print('Error. Retweet to @' + tweet.user.screen_name + ' not successful. Reason: '+error.reason)
            failedtweet = failedtweet + 1

        except StopIteration:
            break

print('\nEnd bot run. Tweets parsed : '+str(validretweet)+', successful : '+str(retweetdone)+' failed : '+str(failedtweet))
