from my_twitter import my_twitter

if __name__ == '__main__':
    search    = "モンハン lang:ja -is:reply -is:retweet -has:links -is:quote"  # search target
    tweet_max = 15 # Number of tweets you want to retrieve (can be set from 10 to 100)
    
    twitter_obj = my_twitter()
    
    search_result = twitter_obj.search_tweets(search,tweet_max)
    
    for tweet_json in search_result:
        print(tweet_json['text'])
        twitter_obj.like_tweet(tweet_json['id'])
    
    # twitter_obj.create_tweet('test')