# Functions to format data
# Author: D.Kisler <admin@dkisler.de>

import pandas as pd
import numpy as np

def list_slit(lst, size=None):
    """
    Function to split range into n sub-ranges, or into m sub-ranges of the size <= size

    :param lst: range to split
    :param size: size of a sub-range
    """

    if not size:
        size = len(lst)

    return [lst[i:i + size] for i in range(0, len(lst), size)]


def dict_keys_formatter(dict):
    """
    Function to remove special characters from json keys

    :param dict: input dictionary

    """

    return {k.replace('.', '_').replace('@', ''): v for k, v in dict.items()}


def dict_subsetter(dict, keys):
    """
    Function to subset the dict by the selected keys

    :param dict: input dictionary
    :param keys: keys to subset initial dict

    """

    return {k: dict[k] for k in keys if k in dict.keys()}


def df_datatypes_downcast(df):
    """
    Function to reduce the allocated memory for numeric data in DataFrame

    :param df: pandas DataFrame
    """

    for col in df.columns:
        col_type = df[col].dtype

        if col_type != object:
            c_min = df[col].min()
            c_max = df[col].max()
            if str(col_type)[:3] == 'int':
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
                elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                    df[col] = df[col].astype(np.int64)
            else:
                if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
                    df[col] = df[col].astype(np.float16)
                elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                    df[col] = df[col].astype(np.float32)
                else:
                    df[col] = df[col].astype(np.float64)
    return True
