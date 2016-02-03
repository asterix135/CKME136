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


def run_query(tweet_id, username, response_list):
    """
    Runs basic Twitter API Query
    Should be rate limited to 180/15 min
    :param tweet_id: integer
    :param response_list: list of response tweets found
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
            response_list.append(line.strip())


def get_sql_records():
    """
    Pulls SQL data of a dumped file so I don't have to deal with Python2
    SQL libraries
    :return: list of dictionaries
    """
    cur_dir = os.getcwd()
    os.chdir('..')
    # sql_file = open('Data/test_stream.txt')
    sql_file = open('Data/sql_dump.txt')
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


def write_bad_image_file(bad_image_list, idx_num):
    cur_dir = os.getcwd()
    os.chdir('..')
    file_name = 'Data/response_data/bad_images' + str(idx_num) + '.txt'
    bad_images = open(file_name, 'w')
    os.chdir(cur_dir)
    for tweet in bad_image_list:
        bad_images.write(str(tweet['tweet_id']) +'\n')
    bad_images.close()


def write_responses(response_list, idx_num):
    cur_dir = os.getcwd()
    os.chdir('..')
    file_name = 'Data/response_data/responses' + str(idx_num) + '.txt'
    responses = open(file_name, 'w')
    os.chdir(cur_dir)
    for tweet in response_list:
        responses.write(str(tweet['id']) + '\t' + tweet['text'] + '\t' +
                        tweet['in_reply_to_status_id'] + '\t' +
                        tweet['created_at'] +'\n')
    responses.close()


def fetch_responses():
    sql_data = get_sql_records()
    response_list = []
    no_image = []
    start_time = time.time()
    processed = 0
    write_file_num = 0
    for tweet in sql_data:
        if is_valid_image(tweet['image_url']):
            run_query(tweet['tweet_id'], tweet['username'], response_list)
            processed += 1
        else:
            no_image.append(tweet)
        if len(response_list) > 100:
            write_responses(response_list, write_file_num)
            response_list = []
            write_file_num += 1
        if len(no_image) > 100:
            write_bad_image_file(no_image, write_file_num)
            no_image = []
            write_file_num += 1
        if processed % 50 == 0:
            print(str(processed) + ' records processed. Up to ' +
                  str(tweet['tweet_id']))
            print('at: ' + time.strftime('%H:%M:%S'))
            print(str(len(no_image)) + ' bad image links found')
            print(str(len(response_list)) + ' responses found\n')

        if time.time() - start_time < 5:
            time.sleep(5 - (time.time() - start_time))
        start_time = time.time()


if __name__ == '__main__':
    print('started at: ' + time.strftime('%H:%M:%S'))
    fetch_responses()