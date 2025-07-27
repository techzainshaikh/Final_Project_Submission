import tweepy
from datetime import datetime
import pandas as pd
import json
import s3fs

# Your Twitter API credentials
access_key = 'f2ZTCjseTI6ClK2hnCGFMo8X2'
secret_access_key = '0ZOXg68PZrPDJv2GlJHuNlMcSCWal5MjrAuDGby0uPSp2UaspQ'
consumer_key = '1940734306122395648-nUs2zoduH0Wr9Ry3PvXd2a65Z5m9F2'
consumer_secret_key = 'seAKS3fwBDDfr9Q9icZgtt288eKynj2svanLiuibMLhK6'
bearer_token='AAAAAAAAAAAAAAAAAAAAAEWQ2wEAAAAAyi0Tq8j77kjOYRa61gXm%2BhOfTZM%3DjYwTdpUr37wIIDfWR05urUcrt8aiNK6ENTq41ALEL05ASBUi0y'

def run_twitter_etl():

    # Replace with your actual Bearer Token from X Developer Portal
    client = tweepy.Client(bearer_token='AAAAAAAAAAAAAAAAAAAAAEWQ2wEAAAAAyi0Tq8j77kjOYRa61gXm%2BhOfTZM%3DjYwTdpUr37wIIDfWR05urUcrt8aiNK6ENTq41ALEL05ASBUi0y')

    # Get user ID from username
    user = client.get_user(username="realdonaldtrump")
    user_id = user.data.id

    # Step 2: Get tweets with necessary fields
    tweets = client.get_users_tweets(
        id=user_id,
        max_results=100,
        tweet_fields=["created_at", "public_metrics","text"]
    )

    # Step 3: Process and save
    lst = []
    if tweets.data:
        for tweet in tweets.data:
            refined_tweet = {
                "user": "realdonaldtrump",
                "text": tweet.text,
                "favorite_count": tweet.public_metrics["like_count"],
                "retweet_count": tweet.public_metrics["retweet_count"],
                "created_at": tweet.created_at
            }
            lst.append(refined_tweet)

        df = pd.DataFrame(lst)
        df.to_csv("s3://twitter-etl-airflow-project-zn/refined_tweets_100.csv", index=False)
        print("Saved to refined_tweets.csv")
    else:
        print("No tweets found.")
