import tweepy
import pymongo
from pymongo import MongoClient

# Twitter API credentials
api_key = 'API_KEY'
api_secret_key = SECRET_API_KEY'
access_token = 'ACESS_TOKEN'
access_token_secret = 'ACCESS_TOKEN_SECRET'

# Authenticate with Twitter
auth = tweepy.OAuthHandler(api_key, api_secret_key)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


# Connect to MongoDB
client = MongoClient('localhost', 27017)
db = client.GeoNews
tweets_collection = db.tweets

# Define a function to fetch tweets
def fetch_tweets(keyword, count=100):
    tweets = api.search_tweets(q=keyword, count=count, lang='en')
    for tweet in tweets:
        data = {
            'text': tweet.text,
            'created_at': tweet.created_at,
            'location': tweet.user.location
        }
        tweets_collection.insert_one(data)

# Fetch disaster-related tweets
fetch_tweets("earthquake OR flood OR hurricane")
