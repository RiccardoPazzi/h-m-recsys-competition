import pandas as pd
import numpy as np

from Data_manager.DatasetMapperManager import DatasetMapperManager

# Constants
timestamp_column = 't_dat'
userid_column = 'customer_id'
itemid_column = 'article_id'
DATASET_NAME = 'hm-exponential-decay15-Validation_salesWeek-Train_3months'


def merge_splits_without_overwrite_origin_dataset(timestamp_df: pd.DataFrame, timestamp_array, columns_name=None):
    """
    :param timestamp_df: The entire timestamp dataframe
    :param timestamp_array: The array of tuples of time intervals that will create the test set
    :param columns_name:
    """
    if columns_name is None:
        columns_name = ["UserID", "ItemID", "Data"]

    final_df = pd.DataFrame(columns=columns_name)

    dropped_timestamp_df = timestamp_df.copy()
    i = 1
    for timeframe in timestamp_array:
        print("Processing interval {}...".format(i))
        i += 1
        t1 = timestamp_df[timestamp_column].searchsorted(timeframe[0])
        t2 = timestamp_df[timestamp_column].searchsorted(timeframe[1])
        cutout = timestamp_df.iloc[t1:t2 - 1]
        dropped_timestamp_df.drop(timestamp_df.index[[t1, t2 - 1]], inplace=True)
        final_df = pd.concat([final_df, cutout])

    return dropped_timestamp_df, final_df


def split_train_validation_multiple_intervals(manager, timestamp_df, timestamp_array_train, timestamp_array_validation,
                                              exponential_decay=30, URM_train='URM_train',
                                              URM_validation='URM_validation'):
    # Retrieve which users fall in the wanted list of time frames
    timestamp_df = timestamp_df.copy()
    print("Preprocessing dataframe...")
    timestamp_df[timestamp_column] = pd.to_datetime(timestamp_df[timestamp_column], format='%Y-%m-%d')

    # timestamp_df.drop('price', inplace=True, axis=1)
    # timestamp_df.drop('sales_channel_id', inplace=True, axis=1)
    timestamp_df.rename(columns={"customer_id": "UserID", "article_id": "ItemID"}, inplace=True)
    timestamp_df['ItemID'] = timestamp_df['ItemID'].astype(str)
    timestamp_df['Data'] = 1.0

    timestamp_df = timestamp_df[[timestamp_column, 'UserID', 'ItemID', 'Data']]

    # Create test/train splits
    rest_interactions, train_interactions = merge_splits_without_overwrite_origin_dataset(timestamp_df,
                                                                                          timestamp_array_train)

    rest_interactions2, validation_interactions = merge_splits_without_overwrite_origin_dataset(timestamp_df,
                                                                                                timestamp_array_validation)

    # Look through the timestamp array to find the last date
    # Assuming the last date is at the end
    finalDate = pd.to_datetime(timestamp_array_train[-1][1])

    dayDifference_df = (train_interactions[timestamp_column] - finalDate).dt.days

    train_interactions['Data'] = np.exp((dayDifference_df / exponential_decay).to_numpy())

    train_interactions.sort_values(by='Data')

    # From graph we can estimate the importance of items goes to 1/e ~ 36% after 6 months that's the reason behind
    # dividing by 180 the number of days
    pd.set_option('display.max_columns', None)
    print(train_interactions.head())
    print(train_interactions.tail())
    print(train_interactions['Data'])
    print(validation_interactions.head())
    print(validation_interactions.tail())

    train_interactions.drop(timestamp_column, inplace=True, axis=1)
    validation_interactions.drop(timestamp_column, inplace=True, axis=1)

    # I keep only the last interaction between a user and a particular item
    train_interactions.drop_duplicates(subset=['UserID', 'ItemID'], keep='last', inplace=True)
    validation_interactions.drop_duplicates(inplace=True)

    manager.add_URM(train_interactions, URM_train)
    manager.add_URM(validation_interactions, URM_validation)


def exponential_decayed_result(timestamp_df, train_timestamp_array, val_timestamp_array, exp_decay):
    # Retrieve which users fall in the wanted list of time frames
    print("Preprocessing dataframe...")
    timestamp_df[timestamp_column] = pd.to_datetime(timestamp_df[timestamp_column], format='%Y-%m-%d')

    timestamp_df.drop('price', inplace=True, axis=1)
    timestamp_df.drop('sales_channel_id', inplace=True, axis=1)
    timestamp_df.rename(columns={"customer_id": "UserID", "article_id": "ItemID"}, inplace=True)
    timestamp_df['ItemID'] = timestamp_df['ItemID'].astype(str)
    timestamp_df['Data'] = 1.0

    timestamp_df = timestamp_df[[timestamp_column, 'UserID', 'ItemID', 'Data']]

    # Create splits
    rest_interactions, train_interactions = merge_splits_without_overwrite_origin_dataset(timestamp_df,
                                                                                          train_timestamp_array)

    rest_interactions2, validation_interactions = merge_splits_without_overwrite_origin_dataset(timestamp_df,
                                                                                                val_timestamp_array)
    # Look through the timestamp array to find the last date
    # Assuming the last date is at the end
    finalDate = pd.to_datetime(train_timestamp_array[-1][1])

    dayDifference_df = (train_interactions[timestamp_column] - finalDate).dt.days

    train_interactions['Data'] = np.exp((dayDifference_df / exp_decay).to_numpy())

    train_interactions.sort_values(by='Data')

    train_interactions.drop(timestamp_column, inplace=True, axis=1)

    validation_interactions.drop(timestamp_column, inplace=True, axis=1)

    # I keep only the last interaction between a user and a particular item
    train_interactions.drop_duplicates(subset=['UserID', 'ItemID'], keep='last', inplace=True)
    validation_interactions.drop_duplicates(inplace=True)

    return train_interactions, validation_interactions


def split_submission_train_intervals(manager, timestamp_df, timestamp_array_train):
    # Retrieve which users fall in the wanted list of time frames
    print("Preprocessing URM_submission dataframe...")
    timestamp_df[timestamp_column] = pd.to_datetime(timestamp_df[timestamp_column], format='%Y-%m-%d')

    # timestamp_df.drop('price', inplace=True, axis=1)
    # timestamp_df.drop('sales_channel_id', inplace=True, axis=1)
    timestamp_df.rename(columns={"customer_id": "UserID", "article_id": "ItemID"}, inplace=True)
    timestamp_df['ItemID'] = timestamp_df['ItemID'].astype(str)
    timestamp_df['Data'] = 1.0

    timestamp_df = timestamp_df[[timestamp_column, 'UserID', 'ItemID', 'Data']]

    df_submission_train = timestamp_df.query(
        "'" + timestamp_array_train[0][0] + "'<=t_dat<'" + timestamp_array_train[0][1] + "'")

    finalDate = pd.to_datetime(timestamp_array_train[0][1])

    dayDifference_df = (df_submission_train[timestamp_column] - finalDate).dt.days

    df_submission_train['Data'] = np.exp((dayDifference_df / 180).to_numpy())

    df_submission_train.sort_values(by='Data')

    df_submission_train.drop(timestamp_column, inplace=True, axis=1)

    df_submission_train.drop_duplicates(subset=['UserID', 'ItemID'], keep='last', inplace=True)

    print(df_submission_train.head())
    print(df_submission_train.tail())

    manager.add_URM(df_submission_train, 'URM_submission_train')


if __name__ == "__main__":
    timestamp_list = [("2019-06-22", "2019-09-23")]
    validation_timestamp = [("2019-09-23", "2019-09-30")]
    transactions = pd.read_csv('../dataset/transactions_train.csv')
    print("Loaded transaction csv...")

    timestamp_list_submission = [("2019-06-22", "2019-09-23")]

    manager = DatasetMapperManager()
    split_train_validation_multiple_intervals(manager, transactions, timestamp_list, validation_timestamp,
                                              exponential_decay=16)
    # split_submission_train_intervals(manager,transactions,timestamp_list_submission)
    # generate dataset with URM (Implicit=True)
    dataset = manager.generate_Dataset(DATASET_NAME, False)
    print("Done! Saving dataset in processed/{}/".format(DATASET_NAME))
    dataset.save_data('../processed/{}/'.format(DATASET_NAME))
    print("Dataset stats:")
    dataset.print_statistics()
    dataset.print_statistics_global()
