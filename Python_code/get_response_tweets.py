try:
    from Python_code import twitter_vals as tv
except:
    import twitter_vals as tv
from TwitterSearch import *
import time
import pymysql.cursors
try:
    from Python_code import sql_vals as sql_vals
except:
    import sql_vals as sql_vals
import urllib.request as urllib
try:
    from Python_code import process_raw_tweets as prt
except:
    import process_raw_tweets as prt

api_key = tv.api_key
api_secret = tv.api_secret
access_token_key = tv.access_token_key
access_token_secret = tv.access_token_secret


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


def write_response_to_mysql(tweet):
    """
    Query twitter for tweets mentioning original poster
    if tweet is in repsonse to original tweet and is not a retweet,
    Add to Reply_tweets table
    :param tweet: dictionary
    :return: nothing
    """
    connection = mysql_connection()
    try:
        with connection.cursor() as cursor:
            id = tweet['id']
            tweet_txt = tweet['text']
            timestamp = prt.convert_twitter_date_to_datetime(tweet['created_at'])
            username = tweet['user']['screen_name']
            sql = "INSERT INTO Reply_tweets (tweet_id, username, text, created_ts) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (id, username, tweet_txt, timestamp))
    except:
        pass
    connection.close()


def pull_tweet_responses(username, tweet_id):
    """
    Queries twitter for tweets mentioning user_id and afer tweet_id
    checks to see if found tweets are in response to tweet_id
    if response and not RT, saves relevant details to SQL database
    :param username:
    :param tweet_id:
    """
    try:
        tso = TwitterSearchOrder()
        tso.set_keywords(['@' + username])
        tso.set_language('en')
        tso.set_since_id(tweet_id)

        ts = TwitterSearch(
                consumer_key=api_key,
                consumer_secret=api_secret,
                access_token=access_token_key,
                access_token_secret=access_token_secret
        )
        for tweet in ts.search_tweets_iterable(tso):
            if tweet['in_reply_to_status_id'] == tweet_id and \
                            tweet['text'][:2] != 'RT':
                write_response_to_mysql(tweet)

    except TwitterSearchException as e:
        print('\nTweet id: ' + str(tweet_id))
        print(e)


def is_valid_image(url):
    """
    Returns boolean as to whether image url is still valid
    :param url: string
    :return: boolean
    """
    try:
        urllib.urlopen(url)
        valid_url = True
    except:
        valid_url = False
    return valid_url


def delete_tweet(tweet_id):
    """
    Deletes one tweet from Original_tweets table in database
    :param tweet_id: integer
    :return: nothing
    """
    connection = mysql_connection()

    with connection.cursor() as cursor:
        sql = 'DELETE FROM Original_tweets WHERE tweet_id = %s'
        cursor.execute(sql, tweet_id)
    connection.commit()
    connection.close()


def pull_all_original_tweets():
    """
    Hardcoded SQL query to pull all originally selected tweets
    checks each image url to ensure still valid
    deletes tweets with invalid images
    returns list of tweets with valid images (tweet_id, username & image_url)
    :return original_tweets: list of dictionaries
    """
    # open database connection
    connection = mysql_connection()

    # pull record id, username and image url from all downloaded tweets
    with connection.cursor() as cursor:
        # sql = "SELECT tweet_id, username, image_url FROM Original_tweets"
        sql = "SELECT tweet_id, username, image_url FROM Original_tweets WHERE tweet_id > 691364559852974080"
        cursor.execute(sql)
        original_tweets = cursor.fetchall()
    connection.close()
    return original_tweets


def get_response_tweets():
    """
    Iterates through all tweets in database 1/minute
    If photo is no longer available, deletes tweet
    Otherwise, looks for responses and adds those to the database
    :return: nothing
    """
    original_tweets = pull_all_original_tweets()
    # one request/minute
    number_processed = 0
    for tweet in original_tweets:
        number_processed += 1
        if number_processed % 10 == 0:
            print("currently on tweet #" + str(number_processed) +
                  '.  Tweet id: ' + str(tweet['tweet_id']))
        if is_valid_image(tweet['image_url']):
            pull_tweet_responses(tweet['username'], tweet['tweet_id'])
            pulled = True
        else:
            delete_tweet(tweet['tweet_id'])
            pulled = False
        if pulled:
            time.sleep(60)



if __name__ == '__main__':
    print('started at: ' + time.strftime('%H:%M:%S'))
    get_response_tweets()
