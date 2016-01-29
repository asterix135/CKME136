"""
Query MySQL database, and one by one query twitter for responses to each tweet

?? Is this rate limited?  If so, to what extent 15/15 minutes?

Options:

?q=@(user who sent tweet)&since_id=(id of tweet)

My solution:
\
Second approach i didnt test yet, but i think it will work as well, is:
1) get user_timeline (https://dev.twitter.com/docs/api/1.1/get/statuses/user_timeline)
2) get user mentions_timeline and repeat as before, this time against user_timeline.


Following is 180/15 or 450/15, not sure which
cf: https://dev.twitter.com/rest/reference/get/search/tweets
GET

https://api.twitter.com/1.1/search/tweets.json?q=%23freebandnames&
since_id=24012619984051000&max_id=250126199840518145&
result_type=mixed&count=4


"""

import oauth2 as oauth
import urllib.request as urllib
import twitter_vals as tv

api_key = tv.api_key
api_secret = tv.api_secret
access_token_key = tv.access_token_key
access_token_secret = tv.access_token_secret

_debug = 0

oauth_token = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_consumer = oauth.Consumer(key=api_key, secret=api_secret)

signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

http_method = "GET"

http_handler = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)


def twitterreq(url, method, parameters):
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


def fetch_responses(username, tweet_id, count=20):
    # url = "https://stream.twitter.com/1/statuses/sample.json"
    url = 'https://api.twitter.com/1.1/search/tweets.json?q=@' + username + \
        '&since_id=' + str(tweet_id) + '&result_type=mixed&count=' + str(count)
    parameters = []
    response = twitterreq(url, "GET", parameters)
    for line in response:
        print(line.strip())

# https://api.twitter.com/1.1/search/tweets.json?q=%23freebandnames&
# since_id=24012619984051000&max_id=250126199840518145&
# result_type=mixed&count=4


def test():
    # fetch_responses('voxdotcom', 692541672274694144)
    fetch_responses('TO_WinterOps', 693052083361189888)

if __name__ == '__main__':
    # fetch_responses()
    test()


