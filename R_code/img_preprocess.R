curwd <- getwd()
setwd('..')
source('Python_code/sql_vals.py')
library(RMySQL)
library(jpeg)
library(caret)

# potential packages: 
# h20 deep learning
# deepnet - in caret package

IMAGE_DIR = '/Volumes/NeuralNet/images/'
SIZE = c(400, 400)


img_to_flat_matrix <- function(filename, size) {
    img <- readJPEG(filename)
    if (length(dim(img)) == 2){
        return(NULL)
    }
    img_wide = as.matrix(img)
    return(img_wide)
}


get_data <- function(class_count=500, image_path=IMAGE_DIR, size=SIZE) {
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
    
    yval <- rep(c(0,1,-1), each=class_count)
    yval_keep <- rep(TRUE, class_count*3)
    
    img_matrix = matrix(nrow=0, ncol=480000)
    
    for (i in 1:length(data)) {
        image <- paste(image_path, data[i,'tweet_id'], '.jpg', sep = '')
        flat <- img_to_flat_matrix(image, size)
        if (is.null(flat)){
            yval_keep[i] = FALSE
            next
        }
        img_matrix <- rbind(img_matrix, flat)
    }
    yval <- yval[yval_keep]
    return (list(img_matrix, yval))
}

x_and_y <- get_data(); x_vals <- x_and_y[1]; y_vals <- x_and_y[2]




setwd(curwd)