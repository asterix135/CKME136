"""
Routines to subset to english tweets that contain original image links
"""
import json
# import calculate_sentiment as cs
# import vader.vader as vs


# TWEET_FILE_PATH = '/Users/christophergraham/Documents/School/Ryerson_program/CKME136/Data/'
TWEET_FILE_PATH = '/Users/chris/Documents/code/misc/CKME136/DATA/'
TWEET_FILE = 'output_jan24.txt'


def subset_tweets(tweet_file):
    """
    Extracts info from json file of twitter data, and subsets
    based on english language and presence of image url
    :param tweet_file: json file
    :return tweets: list of tweets as dictionary
    """
    tweets = []
    for line in tweet_file:
        try:
            curr_tweet = json.loads(line)
            if decide_to_include_tweet(curr_tweet):
                tweets.append(curr_tweet)
        except:
            pass
    return tweets


def decide_to_include_tweet(tweet):
    """
    helper function setting criteria as to whether to include a tweet in
    list to be processed
    :param tweet: dictionary
    :return: boolean
    """
    if 'lang' in tweet and tweet['lang'] == 'en':
        if 'text' in tweet and 'extended_entities' in tweet:
            return True
    return False


def image_is_original(tweet):
    """
    Return boolean as to whether an image is retweeted
    :param tweet: dictionary
    :return: boolean
    """
    # return 'source_user_id_str' in tweet['extended_entities']['media'][0]
    return not tweet['text'][:2] == 'RT'

def count_media_types(tweet_list, print_results=False):
    """
    Calculates number of different types of media files linked in tweets
    Prints results and returns dictionary of counts
    :param tweet_list: list
    :param print_results: Boolean as to whether to print results or not
    :return:
    """
    # The dictionary with media information is
    # tweet['extended_entities']['media'][0]
    all_media_types = {}
    for tweet in tweet_list:
        media_type = tweet['extended_entities']['media'][0]['media_url'][-3:]
        if media_type in all_media_types:
            all_media_types[media_type] += 1
        else:
            all_media_types[media_type] = 1
    if print_results:
        for key in all_media_types:
            print(key + ': ' + str(all_media_types[key]))
    return all_media_types


def convert_twitter_date_to_datetime(twitter_created_at):
    """
    Converts twitter 'created_at' data to UTC-5 datetime format
    :param twitter_created_at:
    :return:
    """
    from datetime import datetime
    from email.utils import parsedate_tz, mktime_tz
    timestamp = mktime_tz(parsedate_tz(twitter_created_at))
    return str(datetime.fromtimestamp(timestamp))


def exploratory():
    tweet_file = open(TWEET_FILE_PATH + TWEET_FILE)
    tweet_list = subset_tweets(tweet_file)
    tweet_file.close()

    # See what we have
    print('Number of tweets with images: ' + str(len(tweet_list)))
    print('image type breakdown')
    all_media_types = count_media_types(tweet_list, True)
    print()

    # does id == id_str??
    matching_ids = 0
    for tweet in tweet_list:
        if tweet['id'] == int(tweet['id_str']):
            matching_ids += 1
    print('Pct matching ids: ' + str(matching_ids / len(tweet_list)) + '\n')

    # How do we find retweet images vs. original images?
    # Count number of tweets with original images
    original_count = 0
    for tweet in tweet_list:
        original_count += image_is_original(tweet)
    print('Nbr tweets with original images: ' + str(original_count) + '\n')

    # Look at some of the data for tweets that have original images
    for tweet in tweet_list[:20]:
        if image_is_original(tweet):
            for key in tweet:
                print(key + ': ' + str(tweet[key]))
            print()
        timestamp = convert_twitter_date_to_datetime(tweet['created_at'])
        print(timestamp)
        print(type(timestamp))
        print('\n\n')

    # Test sentiment
    # for tweet in tweet_list[:50]:
    #     tweet_text = tweet['text']
    #     print(vs.sentiment(tweet_text))
    #     print(tweet_text + '\n')

if __name__ == '__main__':
    exploratory()
