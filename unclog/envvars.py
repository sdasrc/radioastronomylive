from os import environ
CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
ACCESS_KEY = environ['ACCESS_KEY']
ACCESS_SECRET = environ['ACCESS_SECRET']
ASTRO_RADIO_UID = environ['ASTRO_RADIO_UID']

# Files containing the keywords hosted at sdasrc/radioastronomylive-filters
BLOCKUSERFILE = 'https://raw.githubusercontent.com/sdasrc/radioastronomylive-filters/main/blockuser'
BLOCKWORDFILE = 'https://raw.githubusercontent.com/sdasrc/radioastronomylive-filters/main/blockwords'
IGNORETAGFILE = 'https://raw.githubusercontent.com/sdasrc/radioastronomylive-filters/main/ignoretag'
DIRECTACCFILE = 'https://raw.githubusercontent.com/sdasrc/radioastronomylive-filters/main/directaccs'
TOPICFILE = 'https://raw.githubusercontent.com/sdasrc/radioastronomylive-filters/main/topics'
TECHNIQUEFILE = 'https://raw.githubusercontent.com/sdasrc/radioastronomylive-filters/main/techniques'
PUBLISHFILE = 'https://raw.githubusercontent.com/sdasrc/radioastronomylive-filters/main/publishing'
