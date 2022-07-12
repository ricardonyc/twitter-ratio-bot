import configparser
import tweepy

config = configparser.ConfigParser()
config.read("config.ini")


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
        return tweepy.API(auth)

    def recent_mention(self):
        recent_mention = self.api.mentions_timeline(count=1)
        return recent_mention[0]

    def get_mentioned_user(self):
        user = self.recent_mention()
        user_mentioning_bot = user.user.screen_name
        users_list = user.text.split()
        if users_list[-1] == "@ratiocheck":
            return {
                "user_mentioning_bot": user_mentioning_bot,
                "user_to_check": users_list[0].replace("@", ""),
            }
        elif users_list[-1] != "@ratiocheck" and "@" in users_list[-1]:
            return {
                "user_mentioning_bot": user_mentioning_bot,
                "user_to_check": users_list[-1].replace("@", ""),
            }
        else:
            return {
                "user_mentioning_bot": user_mentioning_bot,
                "user_to_check": users_list[0].replace("@", ""),
            }

    def get_users_tweets(self, user):
        return tweepy.Cursor(
            self.api.user_timeline,
            screen_name="Pessi_Grandpa",
            include_rts=False,
            count=5000,
            tweet_mode="extended",
        ).items(5000)

    def get_tweet(self, tweet_id):
        try:
            return {"success": True, "data": self.api.get_status(tweet_id)}
        except:
            return {"success": False, "data": ""}

    def check_if_follows(self):
        user = self.get_mentioned_user()
        username = user["user_mentioning_bot"]
        # print(username)
        follows_data = self.api.get_friendship(target_screen_name=username)
        return {
            "user": follows_data[1].screen_name,
            "follows_you": follows_data[0].followed_by,
        }
