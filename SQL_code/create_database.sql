CREATE DATABASE TwitterImages;
use TwitterImages;

CREATE TABLE Original_tweets(
	tweet_id CHAR(20) PRIMARY KEY,
	username VARCHAR(255),
    text VARCHAR(255),
    processed_text VARCHAR(255),
    image_url varchar(255),
    tweet_sentiment TINYINT,
    unclear_sentiment TINYINT,
    created_ts DATETIME,
    image_hash CHAR(36)
);

CREATE TABLE Image_sizes (
	width INT,
    height INT,
    pixels INT,
    tweet_id CHAR(20) PRIMARY KEY,
    CONSTRAINT Tweet_ref FOREIGN KEY (tweet_id)
		REFERENCES Original_tweets (tweet_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE Duplicate_images(
	tweet_id CHAR(20) PRIMARY KEY,
    primary_tweet CHAR(20),
    username VARCHAR(255),
    text VARCHAR(255),
    processed_text VARCHAR(255),
    image_url VARCHAR(255),
    tweet_sentiment TINYINT,
    unclear_sentiment TINYINT,
    created_ts DATETIME,
    image_hash CHAR(36),
    CONSTRAINT Main_image FOREIGN KEY (primary_tweet)
		REFERENCES Original_tweets (tweet_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE Crowdflower(
	image_id BIGINT PRIMARY KEY,
    sentiment TINYINT,
    unclear_sentiment TINYINT,
    image_url VARCHAR(255)
);