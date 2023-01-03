import tweepy
import requests
from keys import *

class my_twitter:
    def __init__(self):
        self.twitter_client = self.client_info()
    
    def client_info(self):
        client = tweepy.Client(
            bearer_token        = BEARER_TOKEN,
            consumer_key        = CONSUMER_KEY,
            consumer_secret     = CONSUMER_SECRET,
            access_token        = ACCESS_TOKEN,
            access_token_secret = ACCESS_TOKEN_SECRET,
            return_type         = requests.Response,
            wait_on_rate_limit  = True
        )
        
        return client
    
    def search_tweets(self, search, tweet_max):
        tweets = self.twitter_client.search_recent_tweets(query = search, tweet_fields=['author_id', 'created_at'], user_fields=['username', 'name', 'location'], max_results = tweet_max)
        
        tweets_data = tweets.json()['data']
            
        return tweets_data
    
    def create_tweet(self, tweet_text):
        self.twitter_client.create_tweet(text=tweet_text)
        print(f'created tweet({tweet_text})')
        
    def like_tweet(self, tweet_id):
        return self.twitter_client.like(tweet_id)
    

def check_bot(tweets_data):
    result = []
    
    for tweet_json in tweets_data:
        temp_id     = tweet_json['id']
        temp_text   = tweet_json['text']
        for compare_json in tweets_data:
            if(temp_id == compare_json['id']):
                continue
            if(temp_text == compare_json['text']):
                result.append(temp_text)
                
    return result
                