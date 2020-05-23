import pandas as pd

import datetime
import time
CSV_SEPARATOR = ';'

WEATHER_DATA_PATH = './weatherdata'
WEATHER_PAIRS = {
    'Air Temperature': ('airtemp.csv', 'C'),
    'Precipitation': ('precip.csv', 'mm'),
    'Air speed': ('airwind.csv', 'm/s')
}

def load_data(data):
    """
        Data: str of which data to load.

        Loads and returns a pandas dataframe of a given type of data.
    """
    f, unit = WEATHER_PAIRS[data]
    path = f'{WEATHER_DATA_PATH}/{f}'
    df = pd.read_csv(path, sep=CSV_SEPARATOR)
    
    # Create a bunch of new columns with appropriate data and apply a function that turns the data into integer formats
    df[['Year', 'Month', 'Day']] = df['Datum'].str.split('-', expand=True)
    df['Year']  = df['Year'].map(lambda a: int(a))
    df['Month'] = df['Month'].map(lambda a: int(a))
    df['Day']   = df['Day'].map(lambda a: int(a))
    df['Hour']  = df['Tid (UTC)'].map(lambda a: int(a.split(':')[0]))
    
    # Advanced line of code that takes all the columns Year, Month, Day, and Hour and aggregates them into one single separate column called "Timestamp"
    # It turns the Year, Month, Day, and Hour data into a timestamp using the datetime library for easy comparison between different times
    # Making finding interval data very simple
    df['Timestamp'] = df[['Year', 'Month', 'Day', 'Hour']].agg(lambda a: datetime.datetime(*a).timestamp(), axis=1)
    df['Date']      = df[['Year', 'Month', 'Day', 'Hour']].agg(lambda a: ':'.join([str(v) for v in a]), axis=1)
    # Drop the labels we aren't going to use
    df = df.drop(labels=['Tid (UTC)', 'Datum'], axis=1)
    # Rename the label that contains the original data into Value, this column is first as it is originally third but we dropped the labels before it
    # Renaming it since it has a completely "random" name otherwise.
    df = df.rename(columns={df.columns[0]: 'Value'})
    return df, unit

def get_interval(df: pd.DataFrame, min_time: datetime.datetime, max_time: datetime.datetime):
    """
        Takes a dataframe, and two time periods and returns a new dataframe that contains data from the original dataframe that satisfies the time interval.
    """
    # A very advanced expression to finding all the rows that satisfies the given interval
    m = df.loc[(df['Timestamp'] >= min_time.timestamp()) & (df['Timestamp'] <= max_time.timestamp())]  #
    m = m.reset_index(drop=True)
    return m