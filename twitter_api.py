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
    print("USERRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR: ", user)

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
    print("TWEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEET ID: ", tweet_id)
    # * CHECK IF WE RESPONDED TO THE TWEET ALREADY

    user_to_check = user["user_to_check"]
    reply_to_username = user_to_check["screen_name"]
    info = twit.get_user_info_by_username(username=reply_to_username)
    ops_tweets = twit.get_users_tweets(username=user_to_check)

    print("||")
    print("||")
    print(
        "INFOOOOOOOOOOOOOOOOOOOOOOOOooooooooooooooooooooooooooooooOOOOOOOOOOOOO: ", info
    )
    print("||")
    print("||")

    hashtag = twit.get_hashtag()
    print("HASSHHHHHHHHHHHHHHHHTTAGGgGGGGGGGGGGGG: ", hashtag)
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


# #RATIOSTATS
# check the mentions
# if the mentions contains a hashtag, check the hashtag and if its correct,
# respond to the user with a DM about their ratio stats
# grab that user's ID and send that ID a DM with a message

# ! CREATE A METHOD THAT TAKES IN THE USER_ID AND RETURNS ALL THEIR TWEET INFO


# * MENTIONS
# user = twit.get_mentioned_in_tweet()
# print(user)
# tweet_id = user["MOST_RECENT_TWEET_MENTIONED_IN"].in_reply_to_status_id
# print(tweet_id)
# print("USERRRRRRRRRRRRR: ", user)
# print(user)

# tweet_replying_to_id = user["in_reply_to_status_id"] or False
# print(tweet_replying_to_id)

# print(twit.get_mentioned_in_tweet())


# ! GET THE CURRENT TWEET'S ID


# user_to_check = user["user_to_check"]
# reply_to_username = user_to_check["screen_name"]
# info = twit.get_user_info_by_username(username=reply_to_username)
# print("INFOoooooooooooooooooooooooo: ", info.id)


# ops_tweets = twit.get_users_tweets(username=user_to_check)

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

# print("USER----INFOOOOOOOOOOOOO: ", user_info)

# hashtag = twit.get_hashtag()

# print(hashtag)


# ! SENDING DIRECT MESSAGE
# if hashtag == "myratiostats":
#     # send DM
#     # * NEED USER ID
#     # * SEND BACK USER'S RATIO STATS
#     send_dm = twit.send_dm(
#         user_id=user_info["user_id"], message="these are your ratio stats: RATIO!"
#     )
# print(send_dm)


# * USER TAGS YOU AND SAYS #MyRatioStats
# send them a DM with their ratio stats
# their attempts
# their successful ratio's
# their percent success
# measure their 'strenght of ratio's (attempts to success)
# the higher the attempts and the more the success, the better!


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

# df = pandas.DataFrame(tweets)
# print(df)

# df.to_csv("ratios.csv", encoding="utf-8")


# ! CHECK IF THE USER RATIO'D SOMEONE BY REPLYING ONLY WITH '.'
# strip method

# ! CHECK IF USER MENTIONED SOMEONE AFTER YOU OR IF THEY JUST REPLIED TO SOMEONE
# IF THEY JUST REPLIED TO SOMEONE, GET THE FIRST "@" THAT APPEARS IN THE LIST
# IF THEY MENTIONED AN ACCOUNT AFTER MENTIONING YOU, SCAN THAT ACCOUNT
# SCAN THE ACCOUNT AND THEIR REPLIES FOR THE WORD "RATIO" OR A SIMPLE "."
# USE THE lower AND strip METHOD


# * IDEA
# CREATE DATAFRAME
# STORE THE DETAILS OF EVERY USER IN WHICH U CHECK FOR THEIR RATIO STATS
# RANK THE USERS BY SUCCESS PERCENTAGE %
# USER WITH MOST ATTEMPTS AND MOST SUCCESS, IS CROWNED CURRENT RATIO KING
# THE KING IS THEN ANNOUNCED IN A PINNED TWEET
# IN THE TWEET, MENTION THEIR STATS LIKE ATTEMPTS AND SUCCESS RATE AND BIGGEST RATIO SO FAR AGAINST WHOOO???? AND DATE OF RATIO
# ? HOW TO CALCULATE THE STRENGTH OF THEIR RECORD ? LIKE NFL STRENGTH OF SCHEDULE
# scan their tweets and grab the highest ratio rate tweet and save it into the dataframe


# --------------------------------------------------------------------------

# check mentions
# if someone ONLY tags you under a reply, get the INFO of the user that they replied
# to
# scan their account for their ratio stats and then reply to the comment that tagged
# you with the @ of the comment that you were tagged under

# if the mention contains the hashtag #myratiostats
# check the user that mentioned you account and sum up their stats

# create a function that sums up their stats


# -------------------------------------------------------------------------
# create an object of tweets / users DM you replied to
# add a "replied" property and mark it "TRUE"

# each time you reply to someone's tweet, save their TWEET ID
# loop through the last 20 mentions
# if the TWEET ID is found in the saved ID's list, dont respond to the tweet
