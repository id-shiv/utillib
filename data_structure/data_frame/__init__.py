import pandas as pd
import numpy as np


__pandas_version__ = pd.__version__


def to_datetime(dataframe, columns=None, re_index=False):
    if columns:
        if re_index:
            dataframe.index = pd.to_datetime(dataframe[columns])
            return dataframe
        else:
            return pd.to_datetime(dataframe[columns])
    else:
        if re_index:
            dataframe.index = pd.to_datetime(dataframe)
            return dataframe
        else:
            return pd.to_datetime(dataframe)


def data_types(dataframe):
    return dataframe.dtypes


def convert_data_types(dataframe, convert_dict):
    # convert data types (all at once)
    return dataframe.astype(convert_dict)


def load(file_path, category=None):
    if "." in file_path:
        extension = file_path.split('.')[-1]
    else:
        exception_message = 'Unable to retrive extension for file ' + file_path
        print(exception_message)
        return

    # create a category (during file reading)
    if extension == "csv":
        return pd.read_csv(file_path, dtype={category: 'category'})


if __name__ == "__main__":
    print("Pandas Version : " + __pandas_version__)

    URL = 'https://raw.githubusercontent.com/justmarkham/pandas-videos/master/data/drinks.csv'
    dataframe = load(URL, category='continent')
    dataframe = convert_data_types(dataframe, {'beer_servings': 'float', 'spirit_servings': 'float'})
    print(data_types(dataframe))
