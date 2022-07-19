from twit import Twit
import pandas
import snscrape.modules.twitter as sntwitter
import datetime
from helper_functions import responding_comment, read_last_seen, store_last_seen
import time

twit = Twit()

FILE_NAME = "last_seen.txt"


def init():
    user = twit.get_mentioned_in_tweet()

    stored_id = read_last_seen(FILE_NAME)
    if user["id"] == stored_id:
        return
    else:
        store_last_seen(FILE_NAME, user["id"])

    if not user["message"]:
        return

    if not user["follows_you"]:
        return

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


# * ------------------------------------------------------------------------
# * ------------------------------------------------------------------------
# * ------------------------------------------------------------------------
while True:
    init()
    print("init was fired off")
    time.sleep(65)
    print("yeet")
# * ------------------------------------------------------------------------
# * ------------------------------------------------------------------------
# * ------------------------------------------------------------------------
