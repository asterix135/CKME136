"""
Compare various methods to ascribe sentiment to tweets
With aim to figuring out how much they disagree and figuring out what to
do with disagreement
1) read in all tweets
2) Double loop:
    Sentiment methods
        Tweets
            Calculate sentiment
3) For each tweet calculate degree agreement
4) Calculate which method has highest correlation with other methods
5) Dump ambiguous tweets
6) Assign sentiment value based on unanimous agreement
"""

import pymysql.cursors
import pandas as pd
import numpy as np
from Python_code import sql_vals
from Python_code.text_sentiment.vader import vader


def mysql_connection():
    """
    helper function to connect to database
    :return: mysql connection
    """
    connection = pymysql.connect(host=sql_vals.host,
                                 password=sql_vals.password,
                                 port=sql_vals.port,
                                 user=sql_vals.user,
                                 db=sql_vals.db,
                                 cursorclass=pymysql.cursors.DictCursor,
                                 charset='utf8mb4')
    return connection


def pull_all_original_tweets():
    """
    Hardcoded SQL query to pull all originally selected tweets
    :return original_tweets: pandas dataframe of original tweets
    """
    # open database connection
    connection = mysql_connection()

    # pull record id, username and image url from all downloaded tweets
    with connection.cursor() as cursor:
        sql = "SELECT tweet_id, username, text, processed_text " \
              "FROM Original_tweets"
        cursor.execute(sql)
        original_tweets = cursor.fetchall()
    connection.close()
    all_tweets = pd.DataFrame(original_tweets)
    return all_tweets


def return_sentiment_category(score, threshhold):
    """
    Used to determine
    :param score: numeric: value calculated from specific method
    :param threshhold: cutoff value below which sentiment = 0
    :return integer:  -1 (negative), 0 (neutral), 1 (positive)
    """
    if score <= -threshhold:
        return -1
    elif score >= threshhold:
        return 1
    else:
        return 0


def calculate_vader(tweet):
    """
    Calculate sentimenet using VADER code
    :param tweet: tokenizable string
    :return integer: -1 (negative), 0 (neutral), 1 (positive)
    """
    sentiment = vader.sentiment(tweet)['compound']
    return return_sentiment_category(sentiment, 0.1)


def load_afinn_dictionary(sentiment_file_location, splitter = '\t'):
    """
    Creates a sentiment dictionary based on a text file
    dictionary needs to be lines of term and sentiment score
    :param sentiment_file_location: string with location of sentiment data
    :param splitter: text of character to split on = default is tab
    :return sentiment_dictionary: dictionary
    """
    sentiment_file = open(sentiment_file_location)
    sentiment_dictionary = {}
    for line in sentiment_file:
        term, score = line.split(splitter)
        sentiment_dictionary[term] = float(score)
    sentiment_file.close()
    return sentiment_dictionary


def calculate_simple_sentiment(tweet, sentiment_dict):
    """
    calculate sentiment using AFINN lexicon
    :param tweet: string
    :param sentiment_dict: Dictionary with +/- sentiment scores
    :return:
    """
    tokens = tweet.split()
    sentiment = 0
    for word in tokens:
        if word in sentiment_dict:
            sentiment += sentiment_dict[word]
    return return_sentiment_category(sentiment, 1)


def load_huliu_dict(file_location):
    sentiment_dictionary = {}
    negative_words = open(file_location + 'negative-words.txt')
    for line in negative_words:
        if line[0] != ';' and len(line) > 0:
            sentiment_dictionary[line.strip()] = -1
    negative_words.close()

    positive_words = open(file_location + 'positive-words.txt')
    for line in positive_words:
        if line[0] != ';' and len(line) > 0:
            sentiment_dictionary[line.strip()] = 1
    positive_words.close()

    return sentiment_dictionary


def figure_tweet_stats(result_matrix):
    pass


def update_database(result_matrix):
    """
    Updates database to indicate tweet sentiment and whether certainty
    tweet_sentiment: -1 = negative, 0 = neutral, 1 = positive
    unclear_sentiment: 0 = clear, 1 = unclear
    :param result_matrix:
    :return:
    """
    # TODO: Complete this function
    connection = mysql_connection()
    with connection.cursor() as cursor:
        sql = 'UPDATE Original_tweets SET tweet_sentiment = "%s", ' \
              'unclear_sentiment = "%s" WHERE tweet_id = %s'
        clarity = 0
    connection.close()


def calculate_sentiments():
    """
    Loops through various
    :param tweet_list:
    :return:
    """
    # 1. get tweet data into a dataframe
    tweet_df = pull_all_original_tweets()
    # 2. Calculate vader sentiment
    tweet_df['vader'] = tweet_df['processed_text'].apply(calculate_vader)
    # 3. Calculate AFINN sentiment (simple word value count)
    afinn_dict = load_afinn_dictionary('AFINN-111.txt')
    tweet_df['afinn'] = \
        tweet_df['processed_text'].apply(lambda x:
                                         calculate_simple_sentiment(x,
                                                                    afinn_dict))
    # 4. Calculate using Hu/Liu simple +/- word count
    hu_liu_dict = load_huliu_dict('hu_liu/opinion-lexicon-English/')
    tweet_df['huliu'] = \
        tweet_df['processed_text'].apply(
                lambda x: calculate_simple_sentiment(x, hu_liu_dict))

    # 5. identify values with consistent sentiment ratings
    tweet_df['consistent'] = tweet_df.apply(lambda x:
                                            x['vader'] ==
                                            x['afinn'] ==
                                            x['huliu'], axis=1)
    tweet_df['sentiment'] = np.where(tweet_df['consistent'] == True,
                                     tweet_df['vader'], None)
    print('Positive sentiment: ' + str(sum(tweet_df['sentiment'] == 1)))
    print('Negative sentiment: ' + str(sum(tweet_df['sentiment'] == -1)))
    print('Neutral sentiment: ' + str(sum(tweet_df['sentiment'] == 0)))


if __name__ == '__main__':
    calculate_sentiments()
