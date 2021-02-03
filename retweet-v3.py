# Radio Astronomy Live - A Simple Twitter Bot written in Tweepy.
# Written by Soumyadeep Das, IIT Varanasi, India.
# Sunday 05 January 2021 08:11:11 PM IST
# License: MIT License.

import tweepy
from time import sleep
from datetime import datetime, timedelta

# from keys import *
from os import environ
CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
ACCESS_KEY = environ['ACCESS_KEY']
ACCESS_SECRET = environ['ACCESS_SECRET']
ASTRO_RADIO_UID = environ['ASTRO_RADIO_UID']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

searchcount = 200 # Number of tweets to search for in each round
retweetdone = 0 # Retweets done
waittime = 10 # in seconds
oldtweetdays = 1

def splitarr(inparr, nn):
    cc = 0 
    outarr = [] 
    while cc < len(inparr): 
        dd = cc+nn if (cc+nn)<len(inparr) else len(inparr)
        outarr.append(inparr[cc:dd]) 
        cc = dd 
        if cc == len(inparr): 
            break 
    return outarr

lastmsg = int(api.list_direct_messages(1)[0].created_timestamp)
lastmsg = int(lastmsg/1000)
# lastmsg = datetime.timestamp(datetime(2020, 12, 30, 6, 21, 1)) 
lastmsgdt = datetime.fromtimestamp(lastmsg)
lastmsgcutoff = lastmsgdt - timedelta(days=oldtweetdays)
lastmsgcutoff = lastmsgcutoff.strftime("%Y-%m-%d") 

# Create an empty array to which search results will be ADDED
# DO NOT APPEND
search_results = []
ignoretags = ' -AstronomyRadio -nowplaying -fmradio -FM -music -soundcloud -song -album -mixcloud -groove -track -amazon -amzn -playing -play -spotify '

# Search for tagging
key = 'AstronomyRadio OR astronomyradio -filter:retweets AND -filter:replies since:'+lastmsgcutoff
search_results = search_results + api.search(q=key, count=searchcount,tweet_mode='extended')
# print(len(search_results))
# keys =['radio','astronomy','galaxy']
# key = '%2C'.join(keys)

# HASTAG SEARCH #haiku #poetry %23haiku+%23poetry
key = 'radioastronomy OR RadioAstronomy OR RadioAstrophysics OR radioastrophysics OR RadioTelescope OR radiotelescope -filter:retweets AND -filter:replies since:'+lastmsgcutoff
search_results = search_results + api.search(q=key, count=searchcount,tweet_mode='extended')
# print(len(search_results))
# KEYWORD SEARCH
# set(atags).intersection(set(btags))
# RADIO
# 'askap', 'csiro', 

# radio, astronomy (galaxy, OR agn, OR pulsar, OR nebula)
# radio, (astronomy, OR astronomer, OR astrophysics, OR science), (galaxy, OR agn, OR pulsar, OR nebula)

## SEARCH QUERIES

# ONLY RADIO
# Divided into 3 to keep number of args less
print('only radio')
taglist = ['astrochemistry', 'astronomy', 'astronomer', 'astrophysics', 'blackhole', 'black hole', 'black-hole', 'burst', 'chandra', 'cosmology', 'extragalactic', 'exoplanet', 'gravitation', 'gmrt', 'infrared', 'interferometry', 'interferometric', 'iras', 'lofar', 'magnetar', 'NGC', 'nrao', 'nuclei', 'optical','spectroscopy', 'spectroscopic', 'starform', 'synchrotron', 'UGC', 'vlbi' ]
tagarr = splitarr(taglist,9) 
for tags in tagarr:
    srctag = ', OR '.join(tags)
    key = 'radio, ('+srctag+')  '+ignoretags+'  -filter:retweets AND -filter:replies since:'+lastmsgcutoff
    search_results = search_results + api.search(q=key, count=searchcount,tweet_mode='extended')
    print(len(search_results))

# Radio Astronomy Science Paper
print('Radio Astronomy Science Paper')
secondtaglist = ['astronomy', 'astronomer', 'astrophysics', 'science', 'research', 'paper', 'arxiv', 'observation', 'signal','source','object']
secondtags = ', OR '.join(secondtaglist)
taglist = ['agn', 'breakthrough', 'calibration', 'chemistry', 'cluster', 'conference', 'corona', 'cosmic', 'dark','einstein', 'energy', 'epoch', 'evolution', 'feedback', 'galactic', 'galaxy', 'galaxies','gravity','history', 'horizon', 'image', 'jet', 'milky','moon', 'nebula', 'neutrino','newton', 'nobel', 'planet','pulsar', 'relativity', 'satellite','simulation','ska', 'smbh', 'solar' ,'space', 'spectral', 'star', 'stellar','structure', 'supernova', 'sun','universe', 'wide','vla', 'xray','x-ray']
tagarr = splitarr(taglist,9) 
for tags in tagarr:
    srctag = ', OR '.join(tags)
    key = 'radio, ('+secondtags+'), ('+srctag+')  '+ignoretags+'  -filter:retweets AND -filter:replies since:'+lastmsgcutoff
    search_results = search_results + api.search(q=key, count=searchcount,tweet_mode='extended')
    print(len(search_results))

# Radio Astronomy Use Case
print('Radio Use Cases')
secondtaglist = ['3c','atca','breakthrough','chemistry', 'csiro','conference','calibration','dynamics','history','image','imaging','inaf']
secondtags = ', OR '.join(secondtaglist)
taglist = ['agn', 'cluster',  'cosmic', 'corona', 'dark','einstein', 'energy', 'epoch', 'evolution', 'feedback', 'galactic', 'galaxy', 'galaxies','gravity','horizon','jet', 'milky','moon', 'nebula', 'neutrino','newton', 'planet','pulsar', 'relativity', 'smbh', 'solar' , 'star', 'stellar','supernova', 'sun' ]
tagarr = splitarr(taglist,9) 
for tags in tagarr:
    srctag = ', OR '.join(tags)
    key = 'radio, ('+secondtags+'), ('+srctag+')  '+ignoretags+'  -filter:retweets AND -filter:replies since:'+lastmsgcutoff
    search_results = search_results + api.search(q=key, count=searchcount,tweet_mode='extended')
    print(len(search_results))

secondtaglist = ['iras','ngc', 'nrao', 'observ', 'restart','spectral','spectro','simulation', 'ska','structure', 'ugc', 'vla', 'wide', 'xray','x-ray']
secondtags = ', OR '.join(secondtaglist)
for tags in tagarr:
    srctag = ', OR '.join(tags)
    key = 'radio, ('+secondtags+'), ('+srctag+')  '+ignoretags+'  -filter:retweets AND -filter:replies since:'+lastmsgcutoff
    search_results = search_results + api.search(q=key, count=searchcount,tweet_mode='extended')
    print(len(search_results))

print('\nTotal Results : ',str(len(search_results)))

#  and (lastmsgdt < tweet.created_at) 
tweethist = []
for tweet in search_results:
    if (not tweet.retweeted) and ('rt @' not in tweet.full_text.lower()) and ( tweet.id_str not in tweethist ) and (lastmsgdt < tweet.created_at)  and (not tweet.in_reply_to_status_id) and (not tweet.user.screen_name.lower() == 'astronomyradio'):
        try:
            direct_message = api.send_direct_message(ASTRO_RADIO_UID, 'https://twitter.com/'+tweet.user.screen_name+'/status/'+tweet.id_str) 
            print('SENT : @',tweet.user.screen_name)
            #print(tweet.created_at)
            tweethist.append(tweet.id_str)

# Some basic error handling. Will print out why retweet failed, into your terminal.
        except tweepy.TweepError as error:
            print('FAILED : @' + tweet.user.screen_name + ' : '+error.reason)

        except StopIteration:
            break

now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")   
direct_message = api.send_direct_message(ASTRO_RADIO_UID, 'End bot run at '+dt_string+'. . Sent : '+str(len(tweethist))) 
print('\nEnd bot run at '+dt_string+'. . Sent : '+str(len(tweethist))) 
