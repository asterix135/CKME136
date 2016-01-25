"""
Routines to classify and sort text responses to original tweets
"""

import json

TWEET_FILE_PATH = '/Users/christophergraham/Documents/School/Ryerson_program/CKME136/Data/'
TWEET_FILE = 'output_jan24.txt'

def parse_tweets(tweet_file):
    """
    extracts info from file of tweets into a list
    returns the list of a dictionary per tweet
    """
    tweets = []
    for line in tweet_file:
        try:
            tweets.append(json.loads(line))
        except:
            pass
    return tweets


tweet_file = open(TWEET_FILE_PATH + TWEET_FILE)
tweet_list = parse_tweets(tweet_file)
tweet_file.close()
