source('img_preprocess.R')
library(caret)

fitControl <- trainControl( ## 10-fold CV
    method = "repeatedcv",
    number = 10,
    ## repeated ten times
    repeats = 10,
    savePredictions = TRUE)

fit <- train(train_y ~ train_x, method='dnn', trControl = fitControl)
pred_y <- predict(fit, test_x)

cm <- confusionMatrix(pred_y, test_y)
cm$table

