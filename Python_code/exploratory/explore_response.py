import json

# TWEET_FILE_PATH = '/Users/christophergraham/Documents/School/Ryerson_program/CKME136/Data/'
# TWEET_FILE_PATH = '/Users/chris/Documents/code/misc/CKME136/DATA/'
TWEET_FILE_PATH = ''
TWEET_FILE = 'test_response.txt'


def import_data(tweet_file):
    """
    turns json into text
    """
    tweets = []
    for line in tweet_file:
        tweets.append(json.loads(line))
        # try:
        #     tweets.append(json.loads(line))
        # except:
        #     pass
    return tweets


def exploratory():
    tweet_file = open(TWEET_FILE_PATH + TWEET_FILE)
    tweet_list = import_data(tweet_file)
    tweet_file.close()
    for item in tweet_list:
        for key in item:
            print(key + ': ' + str(item[key]))


if __name__ == '__main__':
    exploratory()