curwd <- getwd()
setwd('..')
source('Python_code/sql_vals.py')
library(RMySQL)
library(jpeg)

# potential packages: 
# h20 deep learning
# deepnet - in caret package

IMAGE_DIR = '/Volumes/NeuralNet/images/'


img_to_flat_matrix <- function(filename) {
    img <- readJPEG(filename)
    if (length(dim(img)) == 2){
        return(NULL)
    }
    img_wide = as.matrix(img)
    return(img_wide)
}


get_data <- function(class_count=1000, image_path=IMAGE_DIR) {
    con <- dbConnect(MySQL(),
                     user=user,
                     password=password,
                     dbname=db,
                     host=host,
                     port=port)
    sql <- paste('(SELECT tweet_id, tweet_sentiment FROM Original_tweets',
                 'WHERE unclear_sentiment = 0 AND tweet_sentiment = 0 ',
                 'LIMIT ', class_count, ') ',
                 'UNION ALL ',
                 '(SELECT tweet_id, tweet_sentiment FROM Original_tweets ',
                 'WHERE unclear_sentiment = 0 AND tweet_sentiment = 1 ',
                 'LIMIT ', class_count, ') ',
                 'UNION ALL ',
                 '(SELECT tweet_id, tweet_sentiment FROM Original_tweets ',
                 'WHERE unclear_sentiment = 0 AND tweet_sentiment = -1 ',
                 'LIMIT ', class_count, ')')
    rs <- dbSendQuery(con, sql)
    data <- fetch(rs, n=-1)
    dbDisconnect(con)
    
    for (i in 1:length(data)) {
        image <- paste(image_path, data[i,'tweet_id'], '.jpg', sep = '')
        flat <- img_to_flat_matrix(image)
        if (flat == NULL){
            next
        }
    }
}

setwd(curwd)