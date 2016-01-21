"""
Routines to subset to english tweets that contain image links
"""
import json
import pandas as pd

TWEET_FILE_PATH = '/Users/christophergraham/Documents/School/Ryerson_program/CKME136/Data/'
TWEET_FILE = 'test_output1.txt'


def subset_tweets(tweet_file):
    """
    Extracts info from json file of twitter data, and subsets
    based on english language and presence of image url
    :param tweet_file: json file
    :return:
    """
    tweets = []

    # FOR TESTING - DELETE
    x = 0
    for line in tweet_file:
        try:
            curr_tweet = json.loads(line)
            print(curr_tweet)

            # FOR TESTING - DELETE
            x += 1
            if x > 4:
                break
        except:
            pass
    return tweets


def parse_tweets(tweet_file):
    """
    extracts info from file of tweets into a list
    returns a list with one dictionary per tweet
    """
    tweets = []
    for line in tweet_file:
        try:
            tweets.append(json.loads(line))
        except:
            pass
    return tweets


tweet_file = open(TWEET_FILE_PATH + TWEET_FILE)
# This works but gives all data
# tweet_list = parse_tweets(tweet_file)
# This is a work in progress but is designed to filter down to tweets we want
tweet_list2 = subset_tweets(tweet_file)
tweet_file.close()
