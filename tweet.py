from elasticsearch import Elasticsearch
from elasticsearch import helpers
import tweepy
import boto3

import settings


# Key and Token for twitter api
API_KEY = settings.api_key
API_SECRET = settings.api_secret
ACCESS_TOKEN = settings.access_token
ACCESS_TOKEN_SECRET = settings.access_token_secret
# Amazon ES
ES_HOST = settings.es_host
# Amazon Comprehend
CH_LANG_CODE = settings.ch_lang_code
CH_REGION = settings.ch_region


# Function for detecting sentiment
def detect_sentiment(text):
    comprehend = boto3.client('comprehend', region_name=CH_REGION)
    response = comprehend.detect_sentiment(Text=text, LanguageCode=CH_LANG_CODE)
    return response['Sentiment']


# Function for making es document
def make_document(keyword, count):
    tweets = []
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    i = 0
    for tweet in tweepy.Cursor(api.search, q=keyword).items(count):
        print(i)
        i += 1
        tweet_dic = {
            "@timestamp": tweet.created_at,
            "user_name": tweet.user.name,
            "text": tweet.text,
            "sentiment": detect_sentiment(tweet.text),
            "search_keyword": keyword,
        }
        tweets.append(tweet_dic)

    return tweets


# Function for sending doc to es
def gen_data(docs: dict, index):
    for doc in docs:
        yield {
            "_op_type": "create",
            "_index": index,
            "_source": doc
        }


if __name__ == '__main__':
    tweets = make_document('TOYOTA', 2000)
    es = Elasticsearch(settings.es_host)
    helpers.bulk(es, gen_data(docs=tweets, index='tweet_analysis'))
