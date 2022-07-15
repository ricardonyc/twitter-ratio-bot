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

    if user["send_dm_stats"]:
        # get ID of tweet
        tweet_id = user["MOST_RECENT_TWEET_MENTIONED_IN"].id
        pass

    tweet_id = (
        user["MOST_RECENT_TWEET_MENTIONED_IN"].in_reply_to_status_id
        or user["MOST_RECENT_TWEET_MENTIONED_IN"].id
    )
    stored_id = read_last_seen(FILE_NAME)
    if tweet_id == stored_id:
        return
    store_last_seen(FILE_NAME, tweet_id)
    # * CHECK IF WE RESPONDED TO THE TWEET ALREADY

    user_to_check = user["user_to_check"]
    reply_to_username = user_to_check["screen_name"]
    info = twit.get_user_info_by_username(username=reply_to_username)
    ops_tweets = twit.get_users_tweets(username=user_to_check)

    hashtag = twit.get_hashtag()
    if hashtag == "myratiostats":
        # send DM
        # * NEED USER ID
        # * SEND BACK USER'S RATIO STATS
        try:
            recipient = user["user_mentioning_bot"]
            print("RECIPIENTTTTTTTTTTTTTTTTTTTT: ", recipient)
            response = twit.format_ratio_tweets(user_tweets=ops_tweets)
            message = responding_comment(
                user_to_check=recipient, ratio_stats_list=response
            )
            sent_dm = twit.send_dm(user_id=info.id, message=message)
            print(sent_dm)
            return
        except:
            twit.send_reply(
                tweet_id=tweet_id,
                reply_message="Sorry, couldn't send you a DM for some reason. Make sure your DM's are open and your page isn't private. You might have message requests turned off.",
            )
            return

    store_last_seen(FILE_NAME, tweet_id)
    users_ratio_stats = twit.format_ratio_tweets(user_tweets=ops_tweets)
    responding_message = responding_comment(reply_to_username, users_ratio_stats)

    twit.send_reply(tweet_id=tweet_id, reply_message=responding_message)
    pass


init()


print(
    "------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
)

# ! USER THAT MENTIONED BOT
# RETURNS THEIR USERNAME AND THEIR ID
# user_info = twit.get_latest_user_info()
# user_mentioning_bot_id = user_info["user_id"]
# user_mentioning_bot2 = user_info["username"]
# print(user_mentioning_bot_id)
# print(user_mentioning_bot2)


# hashtag = twit.get_hashtag()

# print(hashtag)


# store_last_seen(FILE_NAME, tweet_id)


# users_ratio_stats = twit.format_ratio_tweets(user_tweets=ops_tweets)


# print(users_ratio_stats)

# * ------------------------------------------------------------------------
# * ------------------------------------------------------------------------
# * ------------------------------------------------------------------------
# while True:
#     time.sleep(5)
#     user = twit.get_mentioned_in_tweet()

#     if not user["message"]:
#         continue

#     user_mentioning_bot = user["user_mentioning_bot"]
#     user_to_check = user["user_to_check"]
#     tweet_mentioned_in_info = user["MOST_RECENT_TWEET_MENTIONED_IN"]

#     ops_tweets = twit.get_users_tweets(username=user_to_check)

#     print(ops_tweets)
#     # ! USER THAT MENTIONED BOT
#     # RETURNS THEIR USERNAME AND THEIR ID
#     most_recent_mention_user_info = twit.get_latest_user_info()
#     recent_mention_user_id = most_recent_mention_user_info["user_id"]
#     recent_mention_username = most_recent_mention_user_info["username"]
#     # print(recent_mention_user_id)
#     # print(recent_mention_username)

#     hashtag = twit.get_hashtag()

#     if not hashtag["hashtag_found"]:
#         continue

#     print(hashtag)

#     users_ratio_stats = twit.format_ratio_tweets(user_tweets=ops_tweets)

#     print(users_ratio_stats)
#     print(responding_comment(user_to_check, users_ratio_stats))
#     print("---------- BEFORE END OF WHILE LOOP ----------")
#     print("---------- END OF WHILE LOOP ----------")
# * ------------------------------------------------------------------------
# * ------------------------------------------------------------------------
# * ------------------------------------------------------------------------


# responding_message = responding_comment(reply_to_username, users_ratio_stats)
# print(responding_message)

# twit.send_reply(tweet_id=tweet_id, reply_message=responding_message)
