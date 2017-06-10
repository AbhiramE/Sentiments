import tweepy
import json
import time
import properties

consumer_key = properties.consumer_key
consumer_secret = properties.consumer_secret
access_key = properties.access_token
access_key_secret = properties.access_token_secret


def search():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_key_secret)

    api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

    searchquery = '"demonetization" OR "demonetisation" OR #demonetization OR #demonetisation -filter:retweets'

    data = api.search(q=searchquery, count=100, lang='en', result_type='mixed')
    data_all = list(data.values())[1]

    while len(data_all) <= 20000:
        time.sleep(5)
        last = data_all[-1]['id']
        data = api.search(q=searchquery, count=100, lang='en', result_type='mixed', max_id=last)
        data_all += list(data.values())[1][1:]

search()