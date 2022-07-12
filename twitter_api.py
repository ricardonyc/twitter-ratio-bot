from twit import Twit
import pandas
import snscrape.modules.twitter as sntwitter
import datetime

months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]

twit = Twit()

# * MENTIONS
user = twit.get_mentioned_user()

# print(user)

print(twit.check_if_follows())


# ! EACH TWEET HAS
# in_reply_to_screen_name - string
# user_mentions - list
# favorite_count - number
# in_reply_to_status_id

users_tweets = twit.get_users_tweets(user["user_to_check"])
# print(users_tweets)

tweets = []


def convert_date(date_created):
    date = str(date_created).split(" ")[0].split("-")
    month = int(date[1]) - 1
    return f"{months[month]} {date[-1]}, {date[0]}"


# GET REPLYING TO TWEET ID
# CHECK GET THE LIKES OF THE TWEET
# for tweet in users_tweets:
#     if "ratio" in tweet.full_text.lower():
#         tweet_replied_to = twit.get_tweet(tweet_id=tweet.in_reply_to_status_id)

#         tweet_replied_to_likes = twit.get_tweet(tweet_id=tweet.in_reply_to_status_id)

#         if tweet_replied_to["success"] and tweet_replied_to_likes["success"]:
#             tweets.append(
#                 {
#                     "user_id": tweet.user.id,
#                     "username": tweet.user.screen_name,
#                     "date_of_tweet": convert_date(tweet.created_at),
#                     "tweet_id": tweet.id,
#                     "tweet": tweet.full_text,
#                     "likes": tweet.favorite_count,
#                     "replying_to_username": tweet.in_reply_to_screen_name or "",
#                     "replying_to_user_id": tweet.in_reply_to_user_id or "",
#                     "replying_to_tweet_id": tweet.in_reply_to_status_id or "",
#                     "tweet_replied_to": tweet_replied_to["data"].text,
#                     "tweet_replied_to_likes": tweet_replied_to_likes[
#                         "data"
#                     ].favorite_count,
#                 }
#             )


# for tweet in tweets:
#     print(tweet)


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
