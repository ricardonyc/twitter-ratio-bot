from twit import Twit
import snscrape.modules.twitter as sntwitter
from helper_functions import responding_comment, read_last_seen, store_last_seen
import time

twit = Twit()

FILE_NAME = "last_seen.txt"


def init():
    # checks what kind of mention it was (direct tweet or in a reply/comment)
    user = twit.get_mentioned_in_tweet()

    # if the user does not specifically mention bot OR does not follow, RETURN
    if not user["message"] or not user["follows_you"]:
        return

    # prevents bot from responding twice
    stored_id = read_last_seen(FILE_NAME)
    if user["id"] == stored_id:
        return
    # stores most recent reply so bot wont reply twice
    else:
        store_last_seen(FILE_NAME, user["id"])

    # makes sure user mentions bot AND the hashtag to send stats through direct messages
    if user["hashtag"]:
        # get users tweets, format, then respond to tweet through direct messages
        user_tweets = twit.get_users_tweets(username=user["username"])
        users_stats = twit.format_ratio_tweets(user_tweets=user_tweets)
        message = responding_comment(
            user_to_check=user["username"], ratio_stats_list=users_stats
        )

        twit.send_dm(user_id=user["user_to_dm"], message=message)
        return

    # responds to a mention in a comment section
    # grabs the user that was mentioned / stats to be checked
    user_to_check = user["data"]["user_to_check"]
    users_tweets = twit.get_users_tweets(username=user_to_check)
    stats = twit.format_ratio_tweets(user_tweets=users_tweets)
    response = responding_comment(user_to_check=user_to_check, ratio_stats_list=stats)
    # sends a comment reply to the user that mentioned the bot
    twit.send_reply(tweet_id=user["id"], reply_message=response)


# runs bot every 2 minutes
while True:
    init()
    time.sleep(120)
