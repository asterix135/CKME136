"""
Get summary stats on all analyzed images from MySQL stored data
"""

import pandas as pd
from Python_code import sql_connect as mysql
import matplotlib.pyplot as plt


def load_image_data():
    connection = mysql.connect()
    with connection.cursor() as cursor:
        sql = 'SELECT * from Image_sizes'
        cursor.execute(sql)
        image_data = cursor.fetchall()
    connection.close()
    return pd.DataFrame(image_data)


def plot_histogram(df, col_name):
    fig, ax = plt.subplots()
    df.hist(col_name, ax=ax)
    fig.savefig(col_name + '_histogram.png')


def generate_summary_stats():
    image_stats = load_image_data()
    # Save size histograms
    plot_histogram(image_stats, 'height')
    plot_histogram(image_stats, 'width')

    # Print Stats
    print('\nAverage original:')
    print(image_stats.mean())
    print('\nStd Dev original:')
    print(image_stats.std())

if __name__ == '__main__':
    generate_summary_stats()