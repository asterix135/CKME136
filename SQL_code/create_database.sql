CREATE DATABASE TwitterImages;
use TwitterImages;

CREATE TABLE Original_tweet(
	tweet_id INTEGER PRIMARY KEY,
    text VARCHAR(255),
    image_url varchar(255),
    tweet_sentiment REAL,
    created_ts DATETIME
);

CREATE TABLE Reply_tweet(
	reply_id INTEGER PRIMARY KEY,
    original_id INTEGER,
    reply_text VARCHAR(255),
    reply_sentiment REAL,
    created_ts DATETIME,
    CONSTRAINT LinkReplies FOREIGN KEY (original_id)
		REFERENCES Original_tweet (tweet_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
    
