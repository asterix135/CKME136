"""
Routines to calculate sentiment for a specific tweet
"""

def calculate_sentiment(tweet, sentiment_dict):
    word_list = tweet.lower().split()
    tweet_value = 0



def create_sentiment_dictionary(sentiment_file_location, splitter='\t'):
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
        sentiment_dictionary[term] = score
    sentiment_file.close()
    return sentiment_dictionary
