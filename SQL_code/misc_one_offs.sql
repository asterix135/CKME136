use TwitterImages;

select count(*) from original_tweets;

SELECT * FROM Original_tweets
	ORDER BY tweet_id DESC
    LIMIT 100;

select * from original_tweets;

set sql_safe_updates = 0;

delete from original_tweets;

INSERT INTO Original_tweets (
	tweet_id, username, text, image_url, created_ts)
    VALUES (123, 
			'testuser',
			'test text', 
            'http://pbs.twimg.com/media/CZg3zEtWYAIC4G9.jpg', 
            '2016-01-24 15:55:40'
);

SELECT * FROM Original_tweets
	WHERE tweet_id = 692541368317665283;

DELETE FROM Original_tweets WHERE tweet_id = 123;

DELETE FROM Original_tweets WHERE tweet_id > 691363834263633921;

ALTER TABLE Original_tweets
	ADD COLUMN unclear_sentiment TINYINT AFTER tweet_sentiment,
    CHANGE COLUMN tweet_sentiment tweet_sentiment TINYINT,
    DROP COLUMN summary_sentiment
;

DROP TABLE Reply_tweets;

ALTER TABLE Original_tweets
	ADD COLUMN processed_text VARCHAR(255) AFTER text;
    
select count(*) from Image_sizes;

delete from Image_sizes;