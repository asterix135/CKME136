curwd <- getwd()
setwd('..')
source('Python_code/sql_vals.py')

library(RMySQL)

# potential packages: 
# h20 deep learning
# mxnet
# darch (may be buggy)
# deepnet - in caret package

con <- dbConnect(MySQL(),
                 user=user,
                 password=password,
                 dbname=db,
                 host=host,
                 port=port)
sql <- paste('(SELECT tweet_id, tweet_sentiment FROM Original_tweets',
             'WHERE unclear_sentiment = 0 AND tweet_sentiment = 0 ',
             'LIMIT ', class_count, ') '
'UNION ALL ' \
'(SELECT tweet_id, tweet_sentiment FROM Original_tweets ' \
  'WHERE unclear_sentiment = 0 AND tweet_sentiment = 1 ' \
  'LIMIT ' + str(class_count) + ') ' \
'UNION ALL ' \
'(SELECT tweet_id, tweet_sentiment FROM Original_tweets ' \
  'WHERE unclear_sentiment = 0 AND tweet_sentiment = -1 ' \
  'LIMIT ' + str(class_count) + ')''

dbDisconnect(con)
