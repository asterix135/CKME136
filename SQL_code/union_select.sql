(SELECT tweet_sentiment, unclear_sentiment
	FROM Duplicate_images
	WHERE primary_tweet = 691363901351526401)

UNION ALL

(SELECT tweet_sentiment, unclear_sentiment
	FROM Original_tweets
    WHERE tweet_id = 691363901351526401)
;