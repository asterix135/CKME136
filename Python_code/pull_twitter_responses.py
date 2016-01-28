"""
Query MySQL database, and one by one query twitter for responses to each tweet

?? Is this rate limited?  If so, to what extent 15/15 minutes?

Options:

?q=@(user who sent tweet)&since_id=(id of tweet)

My solution:
1) get mentions_timeline for the authenticated user (https://dev.twitter.com/docs/api/1.1/get/statuses/mentions_timeline)
2) for every tweet in mentions_timeline: find if this tweet comes in reply to a tweet that was done through our system, using in_reply_to_status_id param, if so save this tweet and connect it to relevant tweet in our system.

Tested this approach and it worked like a charm.

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

import oauthlib.oauth2 as oauth
import urllib
import twitter_vals as tv

api_key = tv.api_key
api_secret = tv.api_secret
access_token_key = tv.access_token_key
access_token_secret = tv.access_token_secret

_debug = 0

# oauth_token = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_token = oauth.OAuth2Token()
oauth_consumer = oauth.Consumer(key=api_key, secret=api_secret)

signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()



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

    opener = urllib.request.OpenerDirector()
    # opener =urllib.OpenerDirector()
    opener.add_handler(http_handler)
    opener.add_handler(https_handler)

    response = opener.open(url, encoded_post_data)

    return response


def fetch_responses():
    # url = "https://stream.twitter.com/1/statuses/sample.json"
    url = 'https://api.twitter.com/1.1/search/tweets.json'
    # parameters = []
    response = twitterreq(url, "GET", parameters)
    for line in response:
        print(line.strip())


# if __name__ == '__main__':
#     fetch_responses()