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

# ! EACH TWEET HAS
# in_reply_to_screen_name - string
# user_mentions - list
# favorite_count - number
# in_reply_to_status_id

users_tweets = twit.get_users_tweets(user)
# print(users_tweets)

# for tweet in users_tweets:
#     print(tweet)

tweets = []

print(
    "------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
)


def convert_date(date_created):
    date = str(date_created).split(" ")[0].split("-")
    month = int(date[1]) - 1
    return f"{months[month]} {date[-1]}, {date[0]}"


tweet = twit.get_tweet(1546580828703977472)
time = str(tweet.created_at).split(" ")[0].split("-")
# print(time)


# GET REPLYING TO TWEET ID
# CHECK GET THE LIKES OF THE TWEET
for tweet in users_tweets:
    if "ratio" in tweet.full_text.lower():
        tweets.append(
            {
                "user_id": tweet.user.id,
                "username": tweet.user.screen_name,
                "date_of_tweet": convert_date(tweet.created_at),
                "tweet_id": tweet.id,
                "tweet": tweet.full_text,
                "likes": tweet.favorite_count,
                "replying_to_username": tweet.in_reply_to_screen_name or "",
                "replying_to_user_id": tweet.in_reply_to_user_id or "",
                "replying_to_tweet_id": tweet.in_reply_to_status_id,
                "tweet_replied_to": twit.get_tweet(tweet.in_reply_to_status_id).text,
                "tweet_replied_to_likes": twit.get_tweet(
                    tweet.in_reply_to_status_id
                ).favorite_count,
            }
        )


# for tweet in tweets:
#     print(tweet)

for tweet in tweets:
    print(tweet)


# df = pandas.DataFrame(tweets)
# print(df)


# tweets = tweepy.Cursor(
#     api.user_timeline,
#     screen_name="Pessi_Grandpa",
#     include_rts=False,
#     count=limit,
#     tweet_mode="extended",
# ).items(limit)

# print(len(tweets))


# for tweet in tweets:
#     print(tweet.full_text)

# users_tweets = api.user_timeline(
#     screen_name="Pessi_Grandpa", include_rts=False, count=1000, tweet_mode="extended"
# )

# print(len(users_tweets))

# for tweet in users_tweets:
#     print(tweet.full_text)

# tweets_list = [
#     tweet.full_text.lower().replace("\n", "").replace("\t", "") for tweet in tweets
# ]

# tweets_list = [tweet for tweet in tweets]

# original_tweet_id = tweets_list[2].in_reply_to_status_id

# twt = api.get_status(original_tweet_id)


# print(tweets_list[2])
# print(twt.text)
# print(twt.favorite_count)


# ! EACH TWEET HAS
# in_reply_to_screen_name - string
# user_mentions - list
# favorite_count - number
# in_reply_to_status_id

# for tweet in tweets_list:
#     if "ratio" in tweet:
#         print(tweet)


# print(tweets_list)
# print(len(tweets_list))
# print(len(users_tweets_list))

# for status in tweepy.Cursor(api.user_timeline).items():
#     # process status here
#     print(status)

# for tweet in users_tweets_list:
#     if "ratio" in tweet:
#         print("ratio found!")
#         print(tweet)

# print(users_tweets_list)

# for tweet in users_tweets:
#     print(tweet.text)


# print(recent_mention[0].text)

# mentioned_user_tweets = api.user_timeline(screen_name='')


# user tweets
# user = "kevinhart4real"
# limit = 25

# tweets = api.user_timeline(screen_name=user, count=limit, tweet_mode="extended")

# for tweet in tweets:
#     print(tweet.full_text)

# public_tweets = api.home_timeline()

# print(public_tweets[0])

# for tweet in public_tweets:
#     print(tweet)

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
