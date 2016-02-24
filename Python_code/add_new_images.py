"""
For adding new images to existing db;
goes through all the previous steps and only saves needed information
"""

from Python_code import twitter_stream as ts
from Python_code import process_raw_tweets as prt
from Python_code.text_sentiment import compare_sentiments as cs
from Python_code.text_sentiment import split_hashtag as sh
from Python_code.images import find_duplicates as dedupe
from Python_code import sql_connect as mysql
from PIL import Image
import json
import time
import requests
from io import BytesIO


# IMAGE_SAVE_PATH = '/Users/chris/Downloads/misc/'
IMAGE_SAVE_PATH = '/Volumes/NeuralNet/images/'


def fetch_image(url):
    try:
        response = requests.get(url)
        if response.status_code == 404 or response.status_code == 403:
            return
        img = Image.open(BytesIO(response.content))
        img = img.resize((400, 400), Image.ANTIALIAS)
        return img
    except:
        return


def add_dupe_to_db(dupe_tweet, match_id, dupe_sentiment, img_hash, proc_txt):
    timestamp = prt.convert_twitter_date_to_datetime(dupe_tweet['created_at'])
    connection = mysql.connect()
    with connection.cursor() as cursor:

        sql = 'INSERT INTO Duplicate_images ( ' \
              'tweet_id, primary_tweet, username, text, processed_text, ' \
              'image_url, tweet_sentiment, created_ts, image_hash, ' \
              'unclear_sentiment) ' \
              'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 0)'
        cursor.execute(sql, (int(dupe_tweet['id']),
                             int(match_id),
                             dupe_tweet['user']['screen_name'],
                             dupe_tweet['text'],
                             proc_txt,
                             dupe_tweet['extended_entities']['media'][0]['media_url'],
                             dupe_sentiment,
                             timestamp,
                             img_hash))
    connection.commit()
    connection.close()


def add_new_record_to_db(tweet, sentiment, img_hash, proc_txt):
    timestamp = prt.convert_twitter_date_to_datetime(tweet['created_at'])
    connection = mysql.connect()
    with connection.cursor() as cursor:
        sql = 'INSERT INTO Original_tweets (' \
              'tweet_id, username, text, processed_text, image_url, ' \
              'tweet_sentiment, unclear_sentiment, created_ts, image_hash) ' \
              'VALUES (%s, %s, %s, %s, %s, %s, 0, %s, %s)'
        cursor.execute(sql, (int(tweet['id']),
                             tweet['user']['screen_name'],
                             tweet['text'],
                             proc_txt,
                             tweet['extended_entities']['media'][0]['media_url'],
                             sentiment,
                             timestamp,
                             img_hash))
    connection.commit()
    connection.close()


def fetchsamples(needed_sent_val=None, max_iters=1000):
    word_list = sh.english_word_list()
    afinn_dict = cs.load_afinn_dictionary('text_sentiment/AFINN-111.txt')
    huliu_dict = \
        cs.load_huliu_dict('text_sentiment/hu_liu/opinion-lexicon-English/')
    url = "https://stream.twitter.com/1/statuses/sample.json"
    parameters = []
    response = ts.twitterreq(url, "GET", parameters)
    num_iters = 0

    for line in response:

        if num_iters > max_iters:
            break

        if isinstance(line, bytes):
            line = line.decode('utf-8')

        # decode if not error message; else wait 1 sec to avoid rate limits
        try:
            tweet = json.loads(line.strip())
        except:
            time.sleep(1)
            print('waiting....')
            continue

        # stop processing if tweet doesn't meet basic criteria
        if not prt.decide_to_include_tweet(tweet):
            continue
        if not prt.image_is_original(tweet):
            continue

        # Calculate tweet sentiment
        tweet_txt = tweet['text']
        cleaned_text = sh.parse_sentence(tweet_txt, word_list)
        vader_sent = cs.calculate_vader(cleaned_text)
        afinn_sent = cs.calculate_simple_sentiment(cleaned_text, afinn_dict)
        hului_sent = cs.calculate_simple_sentiment(cleaned_text, huliu_dict)
        consistent = vader_sent == afinn_sent == hului_sent
        if not consistent:
            continue
        if needed_sent_val and (vader_sent != needed_sent_val):
            continue

        # retrieve and hash image
        image_url = tweet['extended_entities']['media'][0]['media_url']
        img = fetch_image(image_url)
        image_hash = dedupe.calculate_image_hash(img)

        # Ensure not an exact duplicate
        match = dedupe.find_matching_hash(image_hash, tweet['id'])
        if match:
            try:
                add_dupe_to_db(tweet, match, vader_sent,
                               image_hash, cleaned_text)
            except Exception as err:
                print(err)
            continue

        # Save image and write info to db
        try:
            add_new_record_to_db(tweet, vader_sent, image_hash, cleaned_text)
            img.save(IMAGE_SAVE_PATH + tweet['id_str'] + '.jpg')
        except Exception as err:
            print(err)
            continue
        num_iters += 1

    return


if __name__ == '__main__':
    fetchsamples(-1, 5000)
