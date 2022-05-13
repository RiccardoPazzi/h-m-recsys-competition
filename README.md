# Welcome to the H and M recommender systems challenge submission
This project was created during the H and M recommendation challenge on Kaggle, the objective was to recommend clothes to customers using multiple datasets provided by H&M.
The training data consisted of three files:
 - Customers.csv contained information about 1M customers' age, postal code (hashes) and more
 - Articles.csv contained information about clothes such as price, dominant colors, tags
 - Transactions.csv contained all the transactions from 09-2018 up to 09-2020

The objective was to predict transactions for all users in the week after the end of the training set.
Here you'll find a variety of approaches we tried for the competition along some EDA notebooks and useful scripts
Our final best submission was a hybrid model which used exponential decay to weight transactions through time along with 7 other recommenders.
