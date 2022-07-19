from twit import Twit
import snscrape.modules.twitter as sntwitter
from helper_functions import responding_comment, read_last_seen, store_last_seen
import time

twit = Twit()

FILE_NAME = "last_seen.txt"


def init():
    user = twit.get_mentioned_in_tweet()
    # print("USERRRRRRRRrrrrrRRR: ", user)
    # print(user["follows_you"])

    if not user["message"]:
        return

    if not user["follows_you"]:
        return

    stored_id = read_last_seen(FILE_NAME)
    # print(user["id"], stored_id)
    if user["id"] == stored_id:
        print("same ID")
        return
    else:
        store_last_seen(FILE_NAME, user["id"])

    print("checking for hashtag")
    if user["hashtag"]:
        user_tweets = twit.get_users_tweets(username=user["username"])
        users_stats = twit.format_ratio_tweets(user_tweets=user_tweets)
        message = responding_comment(
            user_to_check=user["username"], ratio_stats_list=users_stats
        )

        twit.send_dm(user_id=user["user_to_dm"], message=message)
        return

    user_to_check = user["data"]["user_to_check"]
    users_tweets = twit.get_users_tweets(username=user_to_check)
    stats = twit.format_ratio_tweets(user_tweets=users_tweets)
    response = responding_comment(user_to_check=user_to_check, ratio_stats_list=stats)
    print(response)

    twit.send_reply(tweet_id=user["id"], reply_message=response)
    # print("a reply was sent!!!!!!!!!!!!!!!!!!!!!!!<<<<<<<<<<<<<<<<<<<<<<")


while True:
    print("before init")
    init()
    print("init was fired off")
    time.sleep(120)
    print("after sleep")
