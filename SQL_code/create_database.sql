CREATE DATABASE TwitterImages;
use TwitterImages;

CREATE TABLE Original_tweets(
	tweet_id BIGINT PRIMARY KEY,
	username VARCHAR(255),
    text VARCHAR(255),
    processed_text VARCHAR(255),
    image_url varchar(255),
    tweet_sentiment TINYINT,
    unclear_sentiment TINYINT,
    created_ts DATETIME
);

