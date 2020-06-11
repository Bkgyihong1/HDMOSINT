import os
import tweepy as tw
import json


class twittercollect:
    def __init__(self, username):
        self.username = username
        consumer_key = '#####'  # your consumer key here
        consumer_secret = '#####'  # your consumer secret here
        access_token = '#####'  # your access token here
        access_secret = '#####'  # your access secret here
        # Authorization to consumer key and consumer secret
        auth = tw.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)
        # Access to user's access key and access secret
        auth.set_access_token(access_token, access_secret)
        # Calling api
        self.api = tw.API(auth)
        self.get_profile()
        self.get_tweets()

    # Function to extracttweets
    def get_tweets(self):
        # 1000 tweets to be extracted
        tweets = tw.Cursor(self.api.user_timeline, screen_name=self.username).items(1000)
        tweet_data =[tweet.text for tweet in tweets]
        # Printing the tweets

        print("Collecting tweets")
        self.dump_tweets(tweet_data)
        print(str(len(tweet_data)) + " tweets dumped.")
        print("Successfully saved tweets in " + (os.getcwd()))

    def dump_tweets(self, tweets):
        filename = '../raw_data/tweets.json'
        data = dict()
        data["tweets"] = tweets
        with open(filename, 'w') as fh:
            json.dump(data, fh)
        return filename

    def get_profile(self):
        item = self.api.get_user(self.username)
        name = item.name
        username = item.screen_name
        desc = item.description
        status = str(item.statuses_count)
        followers = str(item.followers_count)
        following = str(item.friends_count)
        print("name: ", name)
        print("screen_name: ", username)
        print("description: ", desc)
        print("statuses_count: ", status)
        print("friends_count: ", following)
        print("followers_count: ", followers)

        profile_data = {
            "name": name,
            "username": username,
            "description": desc,
            "tweet_no": status,
            "following": following,
            "followers": followers
        }

        with open('../raw_data/twitter_profile.json', 'w') as file:
            json.dump(profile_data, file)
        print(f"saved twitter profile data to {os.getcwd()} \ twitter_profile.json.txt")

