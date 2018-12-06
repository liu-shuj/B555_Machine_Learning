IU Bloomington, Machine Learning '18 Fall, Programming Project 4
Shujun Liu (liushuj@iu.edu)

Usage:
Just run "task1.py" or "task2.py"(with python 3.5 or above).

Code structure:
/core/LatentDirichletAllocation.py: implementation of LDA and Bag of Words.
/core/metrics.py: functions that calculates MSE/classification error rate, and data points on learning curves.
/core/bayeslogistic.py: implements Bayes Logistic Regression with 3 updating methods(Newton, GD and SGD); includes training and predicting.
/utils/dataset.py: contains a function that randomly splits the dataset for Cross Validation and a function that draw random subset of specified size from the data set.
/task1.py: code for Task 1.
/task2.py: code for Task 2,
/core/linreg.py: not used; copied from the last programming project.
/core/bingenerative.py: not used; copied from the last programming project.
