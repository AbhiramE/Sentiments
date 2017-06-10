from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from pandas import Series, DataFrame
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

    searchquery = '"demonetization" OR "demonetisation" OR #demonetization OR #demonetisation -"via NMApp" ' \
                  '-filter:retweets'

    data = api.search(q=searchquery, count=100, lang='en', result_type='mixed')
    data_all = list(data.values())[1]
    print(data_all)

    while len(data_all) <= 20000:
        print(len(data_all))
        time.sleep(5)
        last = data_all[-1]['id']
        data = api.search(q=searchquery, count=100, lang='en', result_type='mixed', max_id=last)
        data_all += list(data.values())[1][1:]

    return data_all


def get_sentiment(data):
    tweet = []
    number_favourites = []
    vader_compound = []
    vader_pos = []
    vader_neu = []
    vader_neg = []

    analyser = SentimentIntensityAnalyzer()

    for i in range(0, len(data)):
        tweet.append(data[i]['text'])
        number_favourites.append(data[i]['favorite_count'])
        vader_compound.append(analyser.polarity_scores(data[i]['text'])['compound'])
        vader_pos.append(analyser.polarity_scores(data[i]['text'])['pos'])
        vader_neg.append(analyser.polarity_scores(data[i]['text'])['neg'])
        vader_neu.append(analyser.polarity_scores(data[i]['text'])['neu'])

    twitter_df = DataFrame({'Tweet': tweet,
                            'Favourites': number_favourites,
                            'Compound': vader_compound,
                            'Positive': vader_pos,
                            'Neutral': vader_neu,
                            'Negative': vader_neg})

    twitter_df = twitter_df[['Tweet', 'Favourites', 'Compound',
                             'Positive', 'Neutral', 'Negative']]

    twitter_df.to_csv('Tweets.csv', sep=',', encoding='utf-8')

    return twitter_df


data = search()
get_sentiment(data)

