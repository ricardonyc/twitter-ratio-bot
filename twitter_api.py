import configparser
import tweepy

# read configs
config = configparser.ConfigParser()
config.read("config.ini")

api_key = config["twitter"]["api_key"]
api_key_secret = config["twitter"]["api_key_secret"]

access_token = config["twitter"]["access_token"]
access_token_secret = config["twitter"]["access_token_secret"]

# authentication
auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# user tweets
user = "kevinhart4real"
limit = 25

tweets = api.user_timeline(screen_name=user, count=limit, tweet_mode="extended")

for tweet in tweets:
    print(tweet.full_text)

# public_tweets = api.home_timeline()

# print(public_tweets[0])

# for tweet in public_tweets:
#     print(tweet)
