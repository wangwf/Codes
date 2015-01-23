
## to be test
#  condidate models: linear regression, gbm, cubistModel, rpart, and more
#
#
import graphlab as gl

# load training data
training_column_types = [int,int,int,str, str]
training_sframe = gl.SFrame.read_csv('output.txt', column_type_hints=training_column_types)

# load test data
#test_column_types = [int,int,int, str, str]
#test_sframe = gl.SFrame.read_csv('test.csv', column_type_hints=test_column_types)


# train a model
features = ("response-size Runtime Content-Length request_method Path")


m = gl.boosted_trees.create(training_sframe,
                            features=features, 
                            target='count', objective='regression',
                            num_iterations=100)


import numpy as np
def rmse(predictions, targets):
    return np.sqrt(((predictions - targets) * (predictions - targets)).mean())
pred1 = m.predict(training_sframe)
rmse(training_sframe['count'], pred1)

# predict on test data
prediction = m.predict(test_sframe)
prediction = prediction.astype(int)

