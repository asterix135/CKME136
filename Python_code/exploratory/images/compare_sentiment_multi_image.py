"""
Tests to see how sentiment ratings compare on images that appear
numerous times
"""

from Python_code import sql_connect as mysql
import pandas as pd
import matplotlib.pyplot as plt


def get_unique_repeats():
    connection = mysql.connect()
    with connection.cursor() as cursor:
        sql = 'SELECT DISTINCT primary_tweet, ' \
              'FROM Duplicate_images'
        cursor.execute(sql)
        repeat_df = pd.DataFrame(cursor.fetchall())
    connection.close()
    return repeat_df


def get_all_same(tweet_id):
    connection = mysql.connect()
    with connection.cursor() as cursor:
        sql = 'SELECT unclear_sentiment, tweet_sentiment ' \
              'FROM Duplicate_images ' \
              'WHERE primary_tweet = %s ' \
              'UNION ALL' \
              'SELECT unclear_sentiment, tweet_sentiment ' \
              'FROM Original_tweet ' \
              'WHERE tweet_id = %s'
        cursor.execute(sql, (tweet_id, tweet_id))
        dupes = pd.DataFrame(cursor.fetchall())
    connection.close()

    return dupes


def compare_sentiments():
    repeat_df = get_unique_repeats()
    for i in range(len(repeat_df)):
        cur_img = get_all_same(int(repeat_df.at[i, 'primary_tweet']))
        repeat_df.at[i, 'mode_sent'] = cur_img['tweet_sentiment'].mode()
        repeat_df.at[i, 'mode_clear'] = cur_img['unclear_sentiment'].mode()
        repeat_df.at[i, 'sent_agree'] = sum(cur_img['tweet_sentiment'] ==
                                            repeat_df.at[i, 'mode_sent']) \
                                        / len(cur_img)
        repeat_df.at[i, 'all_agree'] = \
            len(cur_img[(cur_img['tweet_sentiment'] ==
                         repeat_df.at[i, 'mode_sent']) &
                        (cur_img['unclear_sentiment'] ==
                         repeat_df.at[i, 'mode_clear'])]) / len(cur_img)

        print("All sentiment scores match")
        print(sum(repeat_df['sent_agree'] == 1))
        print(str(sum(repeat_df['sent_agree'] == 1) / len(repeat_df)) + '%')
        print('\nComplete score agreement')
        print(sum(repeat_df['all_agree'] == 1))
        print(str(sum(repeat_df['all_agree'] == 1) / len(repeat_df)) + '%')

        # Save Histograms of matches
        plt.figure()
        repeat_df['sent_agree'].plot(kind='hist')
        plt.xlabel('% agreement')
        plt.title('Distribution of sentiment agreement % for duplicate images')
        plt.savefig('sent_agree_histogram.png')

        plt.figure()
        repeat_df['all_agree'].plot(kind='hist')
        plt.xlabel('% agreement')
        plt.title('Distribution of complete agreement % for duplicate images')
        plt.savefig('all_agree_histogram.png')


if __name__ == '__main__':
    compare_sentiments()