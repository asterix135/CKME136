import Python_code.twitter_vals as tv
from TwitterSearch import *
import time
import pymysql.cursors
import Python_code.sql_vals as sql_vals
import urllib.request as urllib
import Python_code.process_raw_tweets as prt

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
    :return:
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
        print('\nTweet id: ' + str(tweet['id']))
        print(e)


def time_control(start_time):
    # 10 second over buffer in case of some kind of lag
    while time.time() - start_time < 90:
        pass
    return True


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
    original_tweets = []
    tweets_to_delete = []
    with connection.cursor() as cursor:
        sql = "SELECT tweet_id, username, image_url FROM Original_tweets"
        cursor.execute(sql)
        original_tweets = cursor.fetchall()
    #     next_tweet = cursor.fetchone()
    #     while next_tweet is not None:
    #         if is_valid_image(next_tweet['image_url']):
    #             original_tweets.append(next_tweet)
    #         else:
    #             tweets_to_delete.append(next_tweet)
    #         next_tweet = cursor.fetchone()
    # # delete tweets with invalid urls from database
    # for tweet in tweets_to_delete:
    #     delete_tweet(connection, tweet['tweet_id'])
    #
    # connection.commit()

    connection.close()
    return original_tweets


def get_response_tweets():
    original_tweets = pull_all_original_tweets()
    # 180 requests per 15 mins - this calculates how many iterations
    add_loop = 0 if len(original_tweets) % 180 == 0 else 1
    num_iterations = int(len(original_tweets)) + add_loop
    for iteration in range(num_iterations):
        start_time = time.time()
        num_processed = 0
        for tweet in original_tweets[iteration * 180:(iteration + 1) * 180]:
            if is_valid_image(tweet['image_url']):
                pull_tweet_responses(tweet['username'], tweet['tweet_id'])
                num_processed += 1
            else:
                delete_tweet(tweet['id'])
        print(num_processed)
        print('time control for iteration' + str(iteration))
        time_control(start_time)


if __name__ == '__main__':
    # # pull_tweet_responses('TO_WinterOps', 693052083361189888)
    # original_tweets = pull_valid_original_tweets()
    # n = int(len(original_tweets)/180) + 1
    # print(n)
    # print(len(original_tweets))
    # print(n * len(original_tweets))
    print('started at: ' + time.strftime('%H:%M:%S'))
    get_response_tweets()
