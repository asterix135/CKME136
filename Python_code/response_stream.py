"""
Run from command line
Need to run as python2 because python3 outputs binary & is a pain to parse
python2 response_stream.py > output_file_name.txt
"""

import oauth2 as oauth
import twitter_vals as tv
import os
import time
import json
try:
    # Python3 library
    import urllib.request as urllib
except:
    # Python2 library
    import urllib2 as urllib


api_key = tv.api_key
api_secret = tv.api_secret
access_token_key = tv.access_token_key
access_token_secret = tv.access_token_secret

_debug = 0

oauth_token = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_consumer = oauth.Consumer(key=api_key, secret=api_secret)

signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

http_method = "GET"


http_handler  = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)


def twitterreq(url, method, parameters):
    """
    Construct, sign and open a twitter request using credentials above
    :param url: request url
    :param method: POST or GET
    :param parameters: (irrelevant, for Posting)
    :return: Twitter response
    """
    req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                                token=oauth_token,
                                                http_method=http_method,
                                                http_url=url,
                                                parameters=parameters)

    req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)

    headers = req.to_header()

    if http_method == "POST":
        encoded_post_data = req.to_postdata()
    else:
        encoded_post_data = None
        url = req.to_url()

    opener = urllib.OpenerDirector()
    opener.add_handler(http_handler)
    opener.add_handler(https_handler)

    response = opener.open(url, encoded_post_data)

    return response


def is_valid_response(json_line, tweet_id):
    """
    Checks to make sure API response is not retweet and is in response
    to original tweet
    :param json_line: json object
    :param tweet_id: integer
    :return: Boolean
    """
    try:
        decoded = json.loads(json_line)['statuses'][0]
        if decoded['in_reply_to_status_id'] == tweet_id and \
            decoded['text'][:2] != 'RT':
            return True
        else:
            return False
    except:
        print('decode failed')
        return False


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


def run_query(tweet_id, username):
    """
    Runs basic Twitter API Query
    Should be rate limited to 180/15 min
    :param tweet_id: integer
    :param username: string
    """
    # url = "https://stream.twitter.com/1/statuses/sample.json"
    base_url = 'https://api.twitter.com/1.1/search/tweets.json?q=@'

    url = base_url + username + '&count=100&since_id=' + str(tweet_id)
    parameters = []
    response = twitterreq(url, "GET", parameters)
    for line in response:
        if is_valid_response(line, tweet_id):
            print(line.strip())


def get_sql_records():
    """
    Pulls SQL data of a dumped file so I don't have to deal with Python2
    SQL libraries
    :return: list of dictionaries
    """
    cur_dir = os.getcwd()
    os.chdir('..')
    sql_file = open('Data/test_stream.txt')
    # sql_file = open('Data/sql_dump.txt')
    os.chdir(cur_dir)
    sql_data = []

    for line in sql_file:
        try:
            record = {}
            record['tweet_id'], record['username'], record['image_url'] = line.split('\t')
            sql_data.append(record)
        except:
            pass
    return sql_data


def write_bad_image_file(bad_image_list):
    cur_dir = os.getcwd()
    os.chdir('..')
    file_name = 'Data/bad_images' + str(idx_num) + '.txt'
    bad_images = open(file_name, 'w')
    os.chdir(cur_dir)
    for tweet in bad_image_list:
        bad_images.write(str(tweet['tweet_id']) +'\n')
    bad_images.close()


def fetch_responses():
    sql_data = get_sql_records()
    num_recs = len(sql_data)
    no_image = []
    start_time = time.time()
    processed = 0
    write_file = 0
    for tweet in sql_data[:1]:
        if is_valid_image(tweet['image_url']):
            run_query(tweet['tweet_id'], tweet['username'])
            processed += 1
        else:
            no_image.append(tweet)

        if time.time() - start_time < 2:
            time.sleep(time.time() - start_time)
        start_time = time.time()


if __name__ == '__main__':
    fetch_responses()