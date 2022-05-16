# H and M fashion recommendation challenge

## Introduction
This project was created during the H and M recommendation challenge on Kaggle, the objective was to recommend clothes to customers using multiple datasets provided by H&M.
The training data consisted of:
 - Customers.csv contained information about customers' age, postal code (hashes) and more (1M rows)
 - Articles.csv contained information about clothes such as price, dominant colors, tags (100K rows)
 - Transactions.csv contained all the transactions from 09-2018 up to 09-2020 (30M rows)
 - A folder containing images of some of the articles

The objective was to predict transactions for all users in the week after the end of the training set.

## Our solution
Here you'll find a variety of approaches we tried for the competition along some EDA notebooks in the EDA folders.
We created a pipeline to simplify operations, which performs the following tasks:
 - Load and clean data (Data_cleaning folder)
 - Create URM/ICM/UCM from clean data, possibly adding modifications such as exponential weighting of transactions. Scripts related to this are contained in the DataProcessing folder
 - Choose and evaluate models, mainly through run_recommenders_on_dataset.py
 - Choose best parameters with Bayesian optimisation
 - Additional analysis: Since the public leaderboard was created on a very small fraction of the dataset (1%) we wanted to estimate lower and upper bounds on the private leaderboard, therefore we created run_5_95_on_recommenders.py which evaluates the models on 5% / 95% pairs of the validation set and provided us with a measure of the variance in the public leaderboard compared to our local results.
 - Create submissions in csv format, both for single models and hybrids

Our final best submission was a hybrid model which used exponential decay to weight transactions through time along with 7 other recommenders.

## Choice of training and validation data
The choice of training and validation data was not obvious since fashion is highly seasonal and moreover we discovered the private test week was during sales season, creating a different data distribution. We decided to use 3 months from June-2019 to 22-Sept-2019 as training and 23-Sept-2019 to 29-Sept-2019 as validation, since also the same week in 2019 was a sales week and we could expect similar distributions. Once we tuned our models using the aforementioned validation we would then retrain using the last three months of the dataset and create submissions for the leaderboard.
This strategy proved effective both for tuning on a "similar" distribution compared to the test set and also by using just three months to avoid recommending non-seasonal items, further EDA justifying our decisions can be found in the SalesEDA folder.

## Technologies
![NumPy](https://img.shields.io/badge/NumPY-%23013243.svg?style=flat&logo=numpy&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-%23150458.svg?style=flat&logo=pandas&logoColor=white)
![AWS](https://img.shields.io/badge/Amazon_AWS-232F3E?style=flat&logo=amazon-aws&logoColor=white)

The models were trained using AWS EC2 due to dataset size.
The project heavily utilizes the library written by [MaurizioFD](https://mauriziofd.github.io/) for the recommender systems course @ Politecnico di Milano, if you want to learn more check the lib folder for additional information.

## Competition
Here is the link to the kaggle competition: [H&M challenge](https://www.kaggle.com/c/h-and-m-personalized-fashion-recommendations)
