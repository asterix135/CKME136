from twitter import *
import twitter_vals as tv

api_key = tv.api_key
api_secret = tv.api_secret
access_token_key = tv.access_token_key
access_token_secret = tv.access_token_secret

t = Twitter(auth=OAuth(access_token_key, access_token_secret, api_key, api_secret))

# foo = t.search.tweets(q='@TO_WinterOps&since_id=693052083361189888&result_type=mixed&count=10')
response_list = t.search.tweets(q='voxdotcom')
for key in response_list:
    print(key + ': ' + str(response_list[key]))
print(len(response_list['statuses']))
bar =  response_list['statuses']
for item in bar:
    print(item)