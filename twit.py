import configparser
import tweepy
from months import months

config = configparser.ConfigParser()
config.read("config/config.ini")


class Twit:
    def __init__(self):
        self.api = self.authenticate_tweepy()

    def __get_api_key(self):
        api_key = config["twitter"]["api_key"]
        api_key_secret = config["twitter"]["api_key_secret"]
        return {"api_key": api_key, "api_key_secret": api_key_secret}

    def __get_access_token(self):
        access_token = config["twitter"]["access_token"]
        access_token_secret = config["twitter"]["access_token_secret"]
        return {
            "access_token": access_token,
            "access_token_secret": access_token_secret,
        }

    def authenticate_tweepy(self):
        keys = self.__get_api_key()
        tokens = self.__get_access_token()
        auth = tweepy.OAuthHandler(keys["api_key"], keys["api_key_secret"])
        auth.set_access_token(tokens["access_token"], tokens["access_token_secret"])
        return tweepy.API(auth, wait_on_rate_limit=True)

    # grabs first mention from notifications
    def recent_mention(self):
        recent_mention = self.api.mentions_timeline(count=1)
        return recent_mention[0]

    # grabs last 15 mentions
    def last_15_mentions(self):
        return self.api.mentions_timeline(count=15)

    def get_mentioned_in_tweet(self):
        user = self.recent_mention()
        user_mentioning_bot = user.user.screen_name
        # makes sure user mentioning bot follows the bot
        follows_you = self.check_if_follows(username=user_mentioning_bot)["follows_you"]
        if not follows_you:
            return {"follows_you": follows_you, "message": False}

        hashtags = [hashtag["text"].lower() for hashtag in user.entities["hashtags"]]
        users_list = user.entities["user_mentions"]
        # makes sure the first mentioned account is the bot and the user used the special hashtag
        if users_list[0]["screen_name"] == "ratiocheck" and "myratiostats" in hashtags:
            return {
                "id": user.user.id,
                "hashtag": True,
                "follows_you": follows_you,
                "user_to_dm": user.user.id,
                "username": user.user.screen_name,
                "message": True,
            }
        # set up info for bot to respond to a mention in a comment section
        elif users_list[0]["screen_name"] != "ratiocheck":
            return {
                "id": user.id,
                "hashtag": False,
                "data": {
                    "user_mentioning_bot": user_mentioning_bot,
                    "user_to_check": user.entities["user_mentions"][0]["screen_name"],
                    "user_id": user.entities["user_mentions"][0]["id"],
                    "respond_to_tweet_id": user.id,
                },
                "follows_you": follows_you,
                "message": True,
            }
        else:
            return {"message": False}

    # gets 5000 of the users most recent tweets
    def get_users_tweets(self, username):
        limit = 5000
        return tweepy.Cursor(
            self.api.user_timeline,
            screen_name=username,
            include_rts=False,
            count=limit,
            tweet_mode="extended",
        ).items(limit)

    def get_tweet(self, tweet_id):
        try:
            return {"success": True, "data": self.api.get_status(tweet_id)}
        except:
            return {"success": False, "data": ""}

    # check if user that mentioned bot follows the bot
    def check_if_follows(self, username):
        follows_data = self.api.get_friendship(target_screen_name=username)
        return {
            "user": follows_data[1].screen_name,
            "follows_you": follows_data[0].followed_by,
        }

    # sends user a reply through direct message
    def send_dm(self, user_id, message):
        return self.api.send_direct_message(recipient_id=user_id, text=message)

    # formats a users tweets to calculate ratio
    def format_ratio_tweets(self, user_tweets):
        tweets = []

        for tweet in user_tweets:
            if "ratio" in tweet.full_text.lower():
                tweet_replied_to = self.get_tweet(tweet_id=tweet.in_reply_to_status_id)

                tweet_replied_to_likes = self.get_tweet(
                    tweet_id=tweet.in_reply_to_status_id
                )

                if tweet_replied_to["success"] and tweet_replied_to_likes["success"]:
                    tweets.append(
                        {
                            "user_id": tweet.user.id,
                            "username": tweet.user.screen_name,
                            "date_of_tweet": self.convert_date(
                                date_created=tweet.created_at
                            ),
                            "tweet_id": tweet.id,
                            "tweet": tweet.full_text,
                            "likes": tweet.favorite_count,
                            "replying_to_username": tweet.in_reply_to_screen_name or "",
                            "replying_to_user_id": tweet.in_reply_to_user_id or "",
                            "replying_to_tweet_id": tweet.in_reply_to_status_id or "",
                            "tweet_replied_to": tweet_replied_to["data"].text,
                            "tweet_replied_to_likes": tweet_replied_to_likes[
                                "data"
                            ].favorite_count,
                        }
                    )
        return self.get_ratio_stats(tweets)

    def convert_date(self, date_created):
        date = str(date_created).split(" ")[0].split("-")
        month = int(date[1]) - 1
        return f"{months[month]} {date[-1]}, {date[0]}"

    #
    def get_ratio_stats(self, tweets_array):
        stats = []

        for tweet in tweets_array:
            stats.append(
                {
                    "ratio_successful": tweet["likes"]
                    > tweet["tweet_replied_to_likes"],
                    "user_likes": tweet["likes"],
                    "tweet_replied_to_likes": tweet["tweet_replied_to_likes"],
                    "ratiod_by_likes": tweet["likes"] - tweet["tweet_replied_to_likes"],
                }
            )

        successful_ratios = 0

        for attempt in stats:
            if attempt["ratio_successful"]:
                successful_ratios += 1

        total_likes_for = 0
        total_likes_against = 0

        for tweet in tweets_array:
            total_likes_for += tweet["likes"]
            total_likes_against += tweet["tweet_replied_to_likes"]

        return {
            "stats": stats,
            "attempted_ratios": len(tweets_array),
            "successful_ratios": successful_ratios,
            "total_likes_for": total_likes_for,
            "total_likes_against": total_likes_against,
        }

    def send_reply(self, tweet_id, reply_message):
        self.api.update_status(
            status=reply_message,
            in_reply_to_status_id=tweet_id,
            auto_populate_reply_metadata=True,
        )
