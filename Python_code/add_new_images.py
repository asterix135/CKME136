"""
For adding new images to existing db;
goes through all the previous steps and only saves needed information
"""

from Python_code import twitter_stream as ts
from Python_code import process_raw_tweets as prt
from Python_code.text_sentiment import compare_sentiments as cs
from Python_code.text_sentiment import split_hashtag as sh
from Python_code.images import find_duplicates as dedupe
from PIL import Image
import json
import time
import requests
from io import BytesIO


IMAGE_SAVE_PATH = '/Users/chris/Downloads/misc/'
# IMAGE_SAVE_PATH = '/Volumes/NeuralNet/images/'


def fetch_image(url):
    try:
        response = requests.get(url)
        if response.status_code == 404 or response.status_code == 403:
            return
        img = Image.open(BytesIO(response.content))
        img = img.resize((400, 400), Image.ANTIALIAS)
        return img
    except Exception:
        return


def fetchsamples(needed_sent_val=None, max_iters = 1000):
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
        except Exception as err:
            time.sleep(1)
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
        if needed_sent_val and vader_sent != needed_sent_val:
            continue

        # retrieve and hash image
        image_url = tweet['extended_entities']['media'][0]['media_url']
        img = fetch_image(image_url)
        image_hash = dedupe.calculate_image_hash(img)
        if dedupe.find_matching_hash(image_hash, tweet['id']):
            #################################
            print('need to do something here')

        # Ensure not an exact duplicate

        # Save image
        # img.save(IMAGE_SAVE_PATH + tweet['id_str'] + '.jpg')
        num_iters += 1

    return


if __name__ == '__main__':
    fetchsamples()
