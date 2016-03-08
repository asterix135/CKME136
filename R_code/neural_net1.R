source('img_preprocess.R')
library(caret)

fitControl <- trainControl( ## 10-fold CV
    method = "repeatedcv",
    number = 10,
    ## repeated ten times
    repeats = 10,
    savePredictions = TRUE)

fit <- train(x=train_x, y=train_y, method='dnn')
pred_y <- predict(fit, test_x)

cm <- confusionMatrix(pred_y, test_y)
cm$table

