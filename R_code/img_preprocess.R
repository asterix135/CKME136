setwd("/Users/christophergraham/Documents/School/Ryerson_program/CKME136/R_code")
curwd <- getwd()
setwd('..')
source('Python_code/sql_vals.py')
setwd(curwd)
library(RMySQL)
library(EBImage)
library(caret)

# potential packages: 
# h20 deep learning
# deepnet - in caret package

IMAGE_DIR = '/Volumes/NeuralNet/images/'
SIZE = c(250, 250)


img_to_flat_matrix <- function(filename, size) {
    img <- readImage(filename)
    img <- resize(img, w=size[1], h=size[2])
    if (length(dim(img)) == 2){
        return(NULL)
    }
    img_wide = as.matrix(img)
    return(img_wide)
}


get_data <- function(class_count=500, image_path=IMAGE_DIR, size=SIZE) {
    # Pull data from database
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
    

    # data = read.table('db_pull_500_each.txt', header=TRUE, 
                      # colClasses = c("character", 'numeric'),
                      # stringsAsFactors = FALSE)  
    # initialize y-value vector
    y_vals <- rep(c(0,1,-1), each=class_count)
    yval_keep <- rep(TRUE, class_count*3)
    
    # initialize matrix for x-values
    img_matrix = matrix(nrow=0, ncol=size[1]*size[2]*3)
    
    # pull image data and update x-value matrix
    for (i in 1:nrow(data)) {
        image <- paste(image_path, data[i,'tweet_id'], '.jpg', sep = '')
        flat <- img_to_flat_matrix(image, size)
        if (is.null(flat)){
            yval_keep[i] = FALSE
            next
        }
        img_matrix <- rbind(img_matrix, t(flat))
    }
    y_vals <- y_vals[yval_keep]
    
    # split test & train sets
    set.seed(3052016)
    train_idx <- createDataPartition(y=y_vals, p=0.8, list = FALSE)
    test_x <- img_matrix[-train_idx,]
    train_x <- img_matrix[train_idx,]
    test_y <- y_vals[-train_idx]
    train_y <- y_vals[train_idx]
    
    preObj <- preProcess(train_x, method=c('pca'), 
                         pcaComp=100)
    test_x <- predict(preObj, test_x)
    train_x <- predict(preObj, train_x)
    
    return (list(test_x, test_y, train_x, train_y))
}

x_and_y <- get_data(class_count=25)
test_x <- x_and_y[[1]]; test_y <- x_and_y[[2]]
train_x <- x_and_y[[3]]; train_y <- x_and_y[[4]]

setwd(curwd)