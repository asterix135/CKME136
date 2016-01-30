CREATE DATABASE TwitterImages;
use TwitterImages;

CREATE TABLE Original_tweets(
	tweet_id BIGINT PRIMARY KEY,
	username VARCHAR(255),
    text VARCHAR(255),
    image_url varchar(255),
    tweet_sentiment REAL,
    summary_sentiment REAL,
    created_ts DATETIME
);

CREATE TABLE Reply_tweets(
	reply_id BIGINT PRIMARY KEY,
    original_id BIGINT,
    username VARCHAR(255),
    reply_text VARCHAR(255),
    reply_sentiment REAL,
    created_ts DATETIME,
    CONSTRAINT LinkReplies FOREIGN KEY (original_id)
		REFERENCES Original_tweets (tweet_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
