# Radio Astronomy Live - A Simple Twitter Bot written in Tweepy.
# Written by Soumyadeep Das, IIT Varanasi, India.
# Sunday 05 January 2021 08:11:11 PM IST
# License: MIT License.

import tweepy
from time import sleep
from datetime import datetime, timedelta
from dateutil.tz import gettz
import rtbottools

# from keys import *
from os import environ
CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
ACCESS_KEY = environ['ACCESS_KEY']
ACCESS_SECRET = environ['ACCESS_SECRET']
ASTRO_RADIO_UID = environ['ASTRO_RADIO_UID']
BLOCKUSERFILE = environ['BLOCKUSERFILE']
BLOCKWORDFILE = environ['BLOCKWORDFILE']
IGNORETAGFILE = environ['IGNORETAGFILE']
DIRECTACCFILE = environ['DIRECTACCFILE']


ignoretagarr = rtbottools.getarrayfromgit(IGNORETAGFILE)
blockedaccs = rtbottools.getarrayfromgit(BLOCKUSERFILE)
filteredkeys = rtbottools.getarrayfromgit(BLOCKWORDFILE)

# from filters import *

MYACCOUNT = 'radioastronlive'
blockedaccs.append(MYACCOUNT)

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

searchcount = 200 # Number of tweets to search for in each round
retweetdone = 0 # Retweets done
waittime = 10 # in seconds
oldtweetdays = 1

lastmsg = int(api.list_direct_messages(1)[0].created_timestamp)
lastmsg = int(lastmsg/1000)
# lastmsg = datetime.timestamp(datetime(2021, 2, 30, 6, 21, 1)) # Uncomment this to use custom cutoff date time for tweets
lastmsgdt = datetime.fromtimestamp(lastmsg)
lastmsgcutoff = lastmsgdt - timedelta(days=oldtweetdays)
lastmsgcutoff = lastmsgcutoff.strftime("%Y-%m-%d") 

# Create an empty array to which search results will be ADDED
# DO NOT APPEND
search_results = []
filtertags = '-filter:retweets AND -filter:replies lang:en '
breakarr = 6
ignoretags = ' -'.join(ignoretagarr)
ignoretags = ' -'+ignoretags+' '

# https://www.patorjk.com/software/taag/#p=display&h=1&f=Big&t=Direct%20Tagging

# =================================================================================
#   _____   _                   _     _______                    _               
#  |  __ \ (_)                 | |   |__   __|                  (_)              
#  | |  | | _  _ __  ___   ___ | |_     | |  __ _   __ _   __ _  _  _ __    __ _ 
#  | |  | || || '__|/ _ \ / __|| __|    | | / _` | / _` | / _` || || '_ \  / _` |
#  | |__| || || |  |  __/| (__ | |_     | || (_| || (_| || (_| || || | | || (_| |
#  |_____/ |_||_|   \___| \___| \__|    |_| \__,_| \__, | \__, ||_||_| |_| \__, |
#                                                   __/ |  __/ |            __/ |
#                                                  |___/  |___/            |___/ 
# =================================================================================

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


# ======================================================================================== 
#                                          _      _____                          _     
#     /\                                  | |    / ____|                        | |    
#    /  \    ___  ___  ___   _   _  _ __  | |_  | (___    ___   __ _  _ __  ___ | |__  
#   / /\ \  / __|/ __|/ _ \ | | | || '_ \ | __|  \___ \  / _ \ / _` || '__|/ __|| '_ \ 
#  / ____ \| (__| (__| (_) || |_| || | | || |_   ____) ||  __/| (_| || |  | (__ | | | |
# /_/    \_\\___|\___|\___/  \__,_||_| |_| \__| |_____/  \___| \__,_||_|   \___||_| |_|
#
# ========================================================================================
                                                                                                                                                                            
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


# ======================================================================================== 
#  _    _              _      _                   _____                          _     
# | |  | |            | |    | |                 / ____|                        | |    
# | |__| |  __ _  ___ | |__  | |_  __ _   __ _  | (___    ___   __ _  _ __  ___ | |__  
# |  __  | / _` |/ __|| '_ \ | __|/ _` | / _` |  \___ \  / _ \ / _` || '__|/ __|| '_ \ 
# | |  | || (_| |\__ \| | | || |_| (_| || (_| |  ____) ||  __/| (_| || |  | (__ | | | |
# |_|  |_| \__,_||___/|_| |_| \__|\__,_| \__, | |_____/  \___| \__,_||_|   \___||_| |_|
#                                         __/ |                                        
#                                        |___/                                         
# ======================================================================================== 


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

# ======================================================================================== 
#   ____          _          _____             _  _        
#  / __ \        | |        |  __ \           | |(_)       
# | |  | | _ __  | | _   _  | |__) | __ _   __| | _   ___  
# | |  | || '_ \ | || | | | |  _  / / _` | / _` || | / _ \ 
# | |__| || | | || || |_| | | | \ \| (_| || (_| || || (_) |
#  \____/ |_| |_||_| \__, | |_|  \_\\__,_| \__,_||_| \___/ 
#                     __/ |                                
#                    |___/                                 
# ======================================================================================== 


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

# ======================================================================================== 
#  _____             _  _          _____                                     _     
# |  __ \           | |(_)        |  __ \                                   | |    
# | |__) | __ _   __| | _   ___   | |__) | ___  ___   ___   __ _  _ __  ___ | |__  
# |  _  / / _` | / _` || | / _ \  |  _  / / _ \/ __| / _ \ / _` || '__|/ __|| '_ \ 
# | | \ \| (_| || (_| || || (_) | | | \ \|  __/\__ \|  __/| (_| || |  | (__ | | | |
# |_|  \_\\__,_| \__,_||_| \___/  |_|  \_\\___||___/ \___| \__,_||_|   \___||_| |_|
# ======================================================================================== 

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

# ======================================================================================== 
#  _____             _  _          _    _               _____                  
# |  __ \           | |(_)        | |  | |             / ____|                 
# | |__) | __ _   __| | _   ___   | |  | | ___   ___  | |      __ _  ___   ___ 
# |  _  / / _` | / _` || | / _ \  | |  | |/ __| / _ \ | |     / _` |/ __| / _ \
# | | \ \| (_| || (_| || || (_) | | |__| |\__ \|  __/ | |____| (_| |\__ \|  __/
# |_|  \_\\__,_| \__,_||_| \___/   \____/ |___/ \___|  \_____|\__,_||___/ \___|
# ======================================================================================== 

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

# ======================================================================================== 
#   _____                   _   __  __                                     
#  / ____|                 | | |  \/  |                                    
# | (___    ___  _ __    __| | | \  / |  ___  ___  ___   __ _   __ _   ___ 
#  \___ \  / _ \| '_ \  / _` | | |\/| | / _ \/ __|/ __| / _` | / _` | / _ \
#  ____) ||  __/| | | || (_| | | |  | ||  __/\__ \\__ \| (_| || (_| ||  __/
# |_____/  \___||_| |_| \__,_| |_|  |_| \___||___/|___/ \__,_| \__, | \___|
#                                                               __/ |      
#                                                              |___/
# ======================================================================================== 

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
if filteredout > 0:
    direct_message = api.send_direct_message(ASTRO_RADIO_UID, filtertweet)  
direct_message = api.send_direct_message(ASTRO_RADIO_UID, dt_string+'. [v] '+str(len(tweethist))+'/'+str(len(search_results))+' [  ] '+str(filteredout)) 
print('\neor@'+dt_string+'. [v] '+str(len(tweethist))+'/'+str(len(search_results))+' [  ] '+str(filteredout)+'.') 
