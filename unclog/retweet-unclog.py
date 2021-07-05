# Radio Astronomy Live - A Simple Twitter Bot written in Tweepy.
# Written by Soumyadeep Das, IIT Varanasi, India.
# Sunday 05 January 2021 08:11:11 PM IST
# License: MIT License.
# List of radio telescopes
# https://en.wikipedia.org/wiki/List_of_radio_telescopes

import tweepy
from time import sleep
from datetime import datetime, timedelta
from dateutil.tz import gettz
import rtbottools     # Essential custommade functions

# Import from keys if you are running locally. Import from 
# environment variables (envvars) if you are running on a 
# remote machine, like Heroku.
localrun = False

if localrun: from keys import * 
else: from envvars import *    

# Retrieve arrays containing blocked accounts and ignored 
# keywords from the public github repo
# https://github.com/sdasrc/radioastronomylive-filters
ignoretagarr = rtbottools.getarrayfromgit(IGNORETAGFILE)
blockedaccs = rtbottools.getarrayfromgit(BLOCKUSERFILE)
filteredkeys = rtbottools.getarrayfromgit(BLOCKWORDFILE)
topiclist = rtbottools.getarrayfromgit(TOPICFILE)
techniquelist = rtbottools.getarrayfromgit(TECHNIQUEFILE)
publishlist = rtbottools.getarrayfromgit(PUBLISHFILE)

# I dont want my posts to come up again
MYACCOUNT = 'radioastronlive'
blockedaccs.append(MYACCOUNT) 

# Authenticating with twitter api
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

# I will search for at max 200 tweets per round, which are less
# than 1 day old. 
# I will wait for 10 seconds before sending each message
searchcount = 200 # Number of tweets to search for in each round
retweetdone = 0 # Retweets done
waittime = 10 # in seconds
oldtweetdays = 1 # Upto how many days in past should I search

# Retrieve last message received time from twitter or
# specify a custom time yourself.
# This time is used to determine the time cutoff, only messages
# sent after the time cutoff are considered
specifycutoffmsgtime = True

today_dt = datetime.today()

if specifycutoffmsgtime:
    lastmsg = datetime.timestamp(datetime(today_dt.year, today_dt.month, today_dt.day - 1, today_dt.hour, today_dt.minute, today_dt.second)) 
else:
    lastmsg = int(api.list_direct_messages(1)[0].created_timestamp)//1000

# Get a cutoff date in YYYY-MM-DD
lastmsgdt = datetime.fromtimestamp(lastmsg)
lastmsgcutoff = lastmsgdt - timedelta(days=oldtweetdays)

print(lastmsgcutoff.strftime("Last msg from %Y-%m-%d %H:%M"))
lastmsgcutoff = lastmsgcutoff.strftime("%Y-%m-%d") 

# Create an empty array to which search results will be ADDED
# DO NOT APPEND
search_results = []
filtertags = '-filter:retweets AND -filter:replies lang:en '
breakarr = 6
ignoretags = ' -'.join(ignoretagarr)
ignoretags = ' -'+ignoretags+' '

# -----------------------------------------
# ACTUAL SEARCHING BEGINS HERE 
# -----------------------------------------

directtags = 0
# Search for tagging
print('Tags search')
key = '@radioastronlive OR #radioastrolive OR #radioastronlive OR @astronomyradio OR #astronomyradio -filter:retweets AND -filter:replies since:'+lastmsgcutoff
search_results = search_results + api.search(q=key, count=searchcount,tweet_mode='extended')
print(len(search_results))
tweethist = []
for tweet in search_results:
    if (not tweet.retweeted) and ('rt @' not in tweet.full_text.lower()) and ( tweet.id_str not in tweethist ) and (lastmsgdt < tweet.created_at)  and (not tweet.in_reply_to_status_id) and (not tweet.user.screen_name.lower() == MYACCOUNT) :
        try:
            direct_message = api.send_direct_message(ASTRO_RADIO_UID, 'https://twitter.com/'+tweet.user.screen_name+'/status/'+tweet.id_str) 
            directtags = 1
            print('\n[v] @',tweet.user.screen_name,' - ',tweet.full_text.replace('\n','... '))
            #print(tweet.created_at)
            tweethist.append(tweet.id_str)

# Some basic error handling. Will print out why retweet failed, into your terminal.
        except tweepy.TweepError as error:
            print('[!] @' + tweet.user.screen_name + ' : '+error.reason)

        except StopIteration:
            break

if(directtags == 1):
    print('AstronomyRadio tags done\n---\n')
    direct_message = api.send_direct_message(ASTRO_RADIO_UID, 'Direct Tags Done\n---\n') 
# print(len(search_results))
# keys =['radio','astronomy','galaxy']
# key = '%2C'.join(keys)


# -----------------------------------------
#     ACCOUNT SEARCHES
# -----------------------------------------
                                                                                                                                                                            
accsearch = 0
# Search for tagging
# (from:TheNRAO OR from:,ICRAR, OR from:SKA_telescope, OR from:ASTRON_NL, OR from:IRA_INAF, OR from:GreenBankObserv, OR from:NCRA_Outreach, OR from:LOFAR, OR from:OgNimaeb, OR from:ColourfulCosmos, OR from:mwatelescope)
print('Specific account search')
accounts = rtbottools.getarrayfromgit(DIRECTACCFILE)   

acckeys = ', OR from:'.join(accounts)
key = acckeys+' -filter:retweets AND -filter:replies since:'+lastmsgcutoff
search_results = []
search_results = search_results + api.search(q=key, count=searchcount,tweet_mode='extended')
print(len(search_results))
tweethist = []
for tweet in search_results:
    if (not tweet.retweeted) and ('rt @' not in tweet.full_text.lower()) and ( tweet.id_str not in tweethist ) and (lastmsgdt < tweet.created_at)  and (not tweet.in_reply_to_status_id) and (not tweet.user.screen_name.lower() == MYACCOUNT.lower()) :
        try:
            direct_message = api.send_direct_message(ASTRO_RADIO_UID, 'https://twitter.com/'+tweet.user.screen_name+'/status/'+tweet.id_str) 
            accsearch = 1
            print('[v] @',tweet.user.screen_name,' - ',tweet.full_text.replace('\n','... '))
            #print(tweet.created_at)
            tweethist.append(tweet.id_str)

# Some basic error handling. Will print out why retweet failed, into your terminal.
        except tweepy.TweepError as error:
            print('[!] @' + tweet.user.screen_name + ' : '+error.reason)

        except StopIteration:
            break

if(accsearch == 1):
    print('AstronomyRadio tags done\n---\n')
    direct_message = api.send_direct_message(ASTRO_RADIO_UID, 'Account Searches Done\n---\n') 


# -----------------------------------------
#     HASHTAG SEARCHING
# -----------------------------------------


# print(len(search_results))
# keys =['radio','astronomy','galaxy']
# key = '%2C'.join(keys)
# HASTAG SEARCH #haiku #poetry %23haiku+%23poetry
print('hashtag search')
key = 'astronomyradio OR radioastronomy OR radioastrolive OR radioastronlive  OR RadioAstronomy OR RadioAstrophysics OR radioastrophysics OR RadioTelescope OR radiotelescope '+filtertags+' since:'+lastmsgcutoff
search_results = []
hashtagsearch = 0
search_results = search_results + api.search(q=key, count=searchcount,tweet_mode='extended')
for tweet in search_results:
    if (not tweet.retweeted) and ('rt @' not in tweet.full_text.lower()) and ( tweet.id_str not in tweethist ) and (lastmsgdt < tweet.created_at)  and (not tweet.in_reply_to_status_id) and (not tweet.user.screen_name.lower() == MYACCOUNT) :
        try:
            direct_message = api.send_direct_message(ASTRO_RADIO_UID, 'https://twitter.com/'+tweet.user.screen_name+'/status/'+tweet.id_str) 
            hashtagsearch = 1
            print('[v] @',tweet.user.screen_name,' - ',tweet.full_text.replace('\n','... '))
            #print(tweet.created_at)
            tweethist.append(tweet.id_str)

# Some basic error handling. Will print out why retweet failed, into your terminal.
        except tweepy.TweepError as error:
            print('[!] @' + tweet.user.screen_name + ' : '+error.reason)

        except StopIteration:
            break

print(len(search_results))
if(hashtagsearch == 1):
    print('Hashtag searches done\n---\n')
    direct_message = api.send_direct_message(ASTRO_RADIO_UID, 'Hashtag searching Done\n---\n') 

# -----------------------------------------
#      ONLY RADIO SEARCH
# -----------------------------------------


# radio, astronomy (galaxy, OR agn, OR pulsar, OR nebula)
# radio, (astronomy, OR astronomer, OR astrophysics, OR science), (galaxy, OR agn, OR pulsar, OR nebula)

## SEARCH QUERIES

# ONLY RADIO
# Divided into 3 to keep number of args less
breakarr = breakarr - 1

search_results = []
print('only radio')
taglist = ['aas','astrochemistry', 'astronomer', 'astronomy', 'astrophoto', 'astrophysics', 'black hole', 'black-hole', 'blackhole', 'blazar', 'burst', 'chandra', 'cosmology', 'exoplanet', 'extragalactic', 'gmrt', 'gravitation', 'infrared', 'interferometric', 'interferometry', 'iras', 'lofar', 'magnetar', 'mpifr', 'NGC', 'nrao', 'nuclei', 'optical', 'quasar', 'spectroscopic', 'spectroscopy', 'starform', 'synchrotron', 'UGC', 'vlbi']
tagarr = rtbottools.splitarr(taglist,breakarr) 
for tags in tagarr:
    srctag = ', OR '.join(tags)
    key = 'radio, ('+srctag+')  '+ignoretags+'  '+filtertags+'since:'+lastmsgcutoff
    search_results = search_results + api.search(q=key, count=searchcount,tweet_mode='extended')
    print(len(search_results))

# -----------------------------------------
#      RADIO RESEARCH
# -----------------------------------------

# Radio Astronomy Science Paper
print('Radio Astronomy Science Paper')
secondtaglist = ['arxiv','astronomer','astronomy','astrophysics','eso','mnras','object','observation','paper','research','science','signal','source','ursi','u.r.s.i']
secondtags = ', OR '.join(secondtaglist)
taglist = ['agn', 'breakthrough', 'calibration', 'chemistry', 'cluster', 'conference', 'corona', 'cosmic', 'dark', 'einstein', 'energy', 'epoch', 'evolution', 'feedback', 'galactic', 'galaxies', 'galaxy', 'gravity', 'history', 'horizon', 'image', 'jet', 'milky', 'moon', 'nebula', 'neutrino', 'newton', 'nobel', 'planet', 'pulsar', 'relativity', 'satellite', 'simulation', 'ska', 'smbh', 'solar' , 'space', 'spectral', 'star', 'stellar', 'structure', 'sun', 'supernova', 'survey', 'universe', 'vla', 'wide', 'x-ray', 'xray']
tagarr = rtbottools.splitarr(taglist,breakarr) 
for tags in tagarr:
    srctag = ', OR '.join(tags)
    key = 'radio, ('+secondtags+'), ('+srctag+')  '+ignoretags+'  '+filtertags+'since:'+lastmsgcutoff
    search_results = search_results + api.search(q=key, count=searchcount,tweet_mode='extended')
    print(len(search_results))

# -----------------------------------------
#      RADIO USEDCASE
# -----------------------------------------

# Radio Astronomy Use Case
print('Radio Use Cases')
secondtaglist = ['3c', 'atca', 'breakthrough', 'calibration', 'chemistry', 'conference', 'csiro', 'dynamics', 'history', 'image', 'images', 'imaging', 'inaf', 'star', 'stellar']
secondtags = ', OR '.join(secondtaglist)
taglist = ['agn', 'cluster', 'corona', 'cosmic', 'dark', 'einstein', 'epoch', 'evolution', 'feedback', 'galactic', 'galaxies', 'galaxy', 'gravity', 'horizon', 'jet', 'milky', 'moon', 'nebula', 'neutrino', 'newton', 'planet', 'pulsar', 'relativity', 'smbh', 'solar' , 'supernova']
tagarr = rtbottools.splitarr(taglist,breakarr) 
for tags in tagarr:
    srctag = ', OR '.join(tags)
    key = 'radio, ('+secondtags+'), ('+srctag+')  '+ignoretags+'  '+filtertags+'since:'+lastmsgcutoff
    search_results = search_results + api.search(q=key, count=searchcount,tweet_mode='extended')
    print(len(search_results))

secondtaglist = ['iras', 'iram', 'ngc', 'nrao', 'observ', 'photo', 'plot', 'restart', 'simulation', 'ska', 'spectral', 'spectro', 'structure', 'ugc', 'vla', 'wide', 'x-ray', 'xray']
secondtags = ', OR '.join(secondtaglist)
for tags in tagarr:
    srctag = ', OR '.join(tags)
    key = 'radio, ('+secondtags+'), ('+srctag+')  '+ignoretags+'  '+filtertags+'since:'+lastmsgcutoff
    search_results = search_results + api.search(q=key, count=searchcount,tweet_mode='extended')
    print(len(search_results))

print('\nTotal Results : ',str(len(search_results)))

# -----------------------------------------
#     SENDING MESSAGES
# -----------------------------------------

#  and (lastmsgdt < tweet.created_at) 
# tweethist = [] # Set to commented after testing done
filteredout = 0
filtertweet = 'List of Filtered Tweets\n'
for tweet in search_results:
    if (not tweet.retweeted) and ('radio' in tweet.full_text.lower()) and ( tweet.id_str not in tweethist ) and (lastmsgdt < tweet.created_at)  and (not tweet.in_reply_to_status_id) and (tweet.user.screen_name.lower() not in blockedaccs) :
        nfound = 1
        for filteredkey in filteredkeys:
            if filteredkey.lower() in tweet.full_text.lower():
                nfound = 0
                break
        if nfound:
            try:
                direct_message = api.send_direct_message(ASTRO_RADIO_UID, 'https://twitter.com/'+tweet.user.screen_name+'/status/'+tweet.id_str) 
                print('\n[v] @',tweet.user.screen_name,' - ',tweet.full_text.replace('\n','... '))
                #print(tweet.created_at)
                tweethist.append(tweet.id_str)

            # Some basic error handling. Will print out why retweet failed, into your terminal.
            except tweepy.TweepError as error:
                print('[!] @' + tweet.user.screen_name + ' : '+error.reason)

            except StopIteration:
                break

        else: 
            filteredout = filteredout + 1
            tfultext = tweet.full_text.replace('\n','... ')
            filtertweet = filtertweet + '['+str(filteredout)+'] '+tweet.user.screen_name+' : '+tfultext+'\n'
            print('\n[  ] @',tweet.user.screen_name,' - ',tweet.full_text)

now = datetime.now(tz=gettz('Asia/Kolkata'))
dt_string = now.strftime("%d/%m %H:%M")      
# if filteredout > 0:
#     direct_message = api.send_direct_message(ASTRO_RADIO_UID, filtertweet)  
direct_message = api.send_direct_message(ASTRO_RADIO_UID, dt_string+'. [v] '+str(len(tweethist))+'/'+str(len(search_results))+' [x] '+str(filteredout)) 
print('\neor@'+dt_string+'. [v] '+str(len(tweethist))+'/'+str(len(search_results))+' [  ] '+str(filteredout)+'.') 
