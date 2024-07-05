import pandas as pd


## filters by age interval
def filter_by_intervals(data: pd.DataFrame, interval: None|list, feature_column: None|str) -> pd.DataFrame:
    """
    Filters the DataFrame based on a feature interval.

    Args:
    data (pd.DataFrame): DataFrame containing the data to be filtered.
    age_range (List[int]): A list of values to filter intervals.

    Returns:
    pd.DataFrame: Filtered DataFrame based on the age feature column.
    """
    if isinstance(interval, list) and len(interval) == 2:
        return data[(data[feature_column] >= interval[0]) & (data[feature_column] <= interval[1])]
    return data


def filter_by_feature(data: pd.DataFrame, feature_list: None|str|list, feature_column: None|str) -> pd.DataFrame:
    """
    Filters the DataFrame based on a list of values within a specified feature column.

    Args:
    data (pd.DataFrame): DataFrame containing the data to be filtered.
    feature_list (List[str]): A list of values to filter within the feature column.
    feature_column (str): The column in the DataFrame to apply the filtering.

    Returns:
    pd.DataFrame: Filtered DataFrame based on the specified feature column and list of values.
    """
    if feature_list:
        if isinstance(feature_list, str):
            feature_list = [feature_list]
        return data[data[feature_column].isin(feature_list)]
    return data

