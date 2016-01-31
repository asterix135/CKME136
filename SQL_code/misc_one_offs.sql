drop database TwitterImages;

select count(*) from original_tweets;

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
	WHERE tweet_id = 123;

DELETE FROM Original_tweets WHERE tweet_id = 123;

DELETE FROM Original_tweets WHERE tweet_id > 691363834263633921;

SELECT COUNT(*) FROM Reply_tweets;