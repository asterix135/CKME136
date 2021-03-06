"""
Run from command line
works as either python 2 or 3
python twitter_stream.py > output_file_name.txt
"""

import oauth2 as oauth
# to run as python2
try:
    import urllib2 as urllib
except:
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


http_handler  = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)

'''
Construct, sign, and open a twitter request
using the hard-coded credentials above.
'''
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

def fetchsamples():
    url = "https://stream.twitter.com/1/statuses/sample.json"
    #url = 'https://api.twitter.com/1.1/search/tweets.json?q=birthday'
    parameters = []
    response = twitterreq(url, "GET", parameters)
    for line in response:
        if isinstance(line, bytes):
            line = line.decode('utf-8')
        print(line.strip())

if __name__ == '__main__':
    fetchsamples()
