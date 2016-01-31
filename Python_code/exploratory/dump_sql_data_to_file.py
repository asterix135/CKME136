import pymysql.cursors
import os
try:
    from Python_code import sql_vals as sql_vals
except:
    import sql_vals as sql_vals



def mysql_connection():
    """
    helper function to connect to database
    :return: mysql connection
    """
    connection = pymysql.connect(host=sql_vals.host,
                             password=sql_vals.password,
                             port=sql_vals.port,
                             user=sql_vals.user,
                             db=sql_vals.db,
                             cursorclass=pymysql.cursors.DictCursor,
                             charset='utf8mb4')
    return connection


def pull_all_original_tweets():
    """
    Hardcoded SQL query to pull all originally selected tweets
    checks each image url to ensure still valid
    deletes tweets with invalid images
    returns list of tweets with valid images (tweet_id, username & image_url)
    :return original_tweets: list of dictionaries
    """
    # open database connection
    connection = mysql_connection()

    # pull record id, username and image url from all downloaded tweets
    with connection.cursor() as cursor:
        # sql = "SELECT tweet_id, username, image_url FROM Original_tweets"
        sql = "SELECT tweet_id, username, image_url FROM Original_tweets"
        cursor.execute(sql)
        original_tweets = cursor.fetchall()
    connection.close()

    cur_dir = os.getcwd()
    os.chdir('..')
    os.chdir('..')
    dump_file = open('Data/sql_dump.txt', 'w')
    os.chdir(cur_dir)
    for tweet in original_tweets:
        dump_file.write(str(tweet['tweet_id']) + '\t' + tweet['username'] +
                        '\t' + tweet['image_url'] + '\n')
    dump_file.close()
    os.chdir(cur_dir)

    return original_tweets


if __name__ == '__main__':
    pull_all_original_tweets()
