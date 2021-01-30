# Radio Astronomy Live - A Simple Twitter Bot written in Tweepy

This is **Radio Astronomy Live**, a non-spammy twitter bot written in [Tweepy](http://www.tweepy.org/). The bot is run periodically on a [Heroku](https://heroku.com) Dyno.

## How does it work?
Radio Astronomy Live is a simple python script that iteratively searches for tweets with the `radio astronomy` keyword. These tweets are further filtered using a list of keywords in order to exclude false hits.

The current list of keywords is given below.

`    active, agn, arxiv, astro, astronomy, extragalac, galax, gmrt, jet, lofar, milky, NGC, nrao, observ, paper, pulsar, radio, radio-astro, radioastro, research, signal, ska, solar, star, sun, supernova, telescope, vla, vlbi`

The bot also searches for `@AstronomyRadio` and `#AstronomyRadio` tags.

* Suggest new keywords by [opening a new issue](https://github.com/dassoumyadeep/radioastronomylive/issues/new).


## How to run this bot locally?

*Understand [Twitter's Rules on Automation](https://support.twitter.com/articles/76915) before starting.*

* Install tweepy. 

`   pip install tweepy`

* Sign up for a Twitter Developer account and create a new application [here](https://apps.twitter.com/app/new). A Twitter application is essentially your 'bot' - it will send tweets, direct message, reply, retweet, follow and search Twitter from any email inbox. Generate your a consumer key, consumer secret, access key, and access secret. This bot requires both READ and WRITE Permissions enabled to work.

*For your own safety, do not save the keys with the bot. Keep them in a separate file and add it to .gitignore, or store the keys as system variables.*

* `retweet.py` is the python script that you would run. The script uses Python 3+. Edit the script according to your needs.

* Searching for a single keywords often results in a  large number of irrelevant results. It is therefore advisable to use a secondary set of filters. Update the `keydict` variable in `retweet.py` with relevant keywords.

* Run the bot by

`   python retweet.py`

## Optional - Setting up a Heroku repo

* I use the [Flask](https://flask.palletsprojects.com/en/1.1.x/) environment to create a web server in `server.py`. Feel free to switch to other environments such as Django. [Here](https://devcenter.heroku.com/articles/getting-started-with-python) is the Heroku documentation.

* Define these dependancies in `requirements.txt` in the root directory.

```
    Flask
    heroku
    tweepy
```

* Setup the server and the worker in `Procfile` as

```
    web: python server.py
    worker: python retweet.py 
```

* Push to Heroku repo. Add a scheduler to run it regularly. Heroku has its limitations. Alternatively, consider Cron Job to automate things, or use a Raspberry Pi to keep it alive at all times.


## Support

* Suggest new keywords or report issues by [opening a new issue](https://github.com/dassoumyadeep/radioastronomylive/issues/new).

* Alternatively, [mail me](mailto:soumyadeep.das.phy14@iitbhu.ac.in?subject=[GitHub]%20Radio%20Astronomy%20Live) to report an issue or collaborate. 
