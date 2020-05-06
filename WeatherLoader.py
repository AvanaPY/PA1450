import pandas as pd
import matplotlib.pyplot as plt
import datetime
import time
CSV_SEPARATOR = ';'

WEATHER_DATA_PATH = './weatherdata'
WEATHER_PAIRS = {
    'airtemp': 'airtemp.csv',
    'precip': 'precip.csv'
}

def load_data(data):
    """
        Data: str of which data to load.

        Loads and returns a pandas dataframe of a given type of data.
    """
    path = f'{WEATHER_DATA_PATH}/{WEATHER_PAIRS[data]}'
    df = pd.read_csv(path, sep=CSV_SEPARATOR)
    
    df['Year'], df['Month'], df['Day'] = df['Datum'].str.split('-').str

    # Create a bunch of new columns with appropriate data and apply a function that turns the data into integer formats
    df['Year']  = df['Year'].map(lambda a: int(a.split(':')[0]))
    df['Month'] = df['Month'].map(lambda a: int(a.split(':')[0]))
    df['Day']   = df['Day'].map(lambda a: int(a.split(':')[0]))
    df['Hour'] = df['Tid (UTC)'].map(lambda a: int(a.split(':')[0]))
    
    # Advanced line of code that takes all the columns Year, Month, Day, and Hour and aggregates them into one single separate column called "Whole"
    # It turns the Year, Month, Day, and Hour data into a timestamp using the datetime library for easy comparison between different times
    # Making finding interval data very simple
    df['Whole'] = df[['Year', 'Month', 'Day', 'Hour']].agg(lambda a: datetime.datetime(*a).timestamp(), axis=1)

    # Drop the labels we aren't going to use
    df = df.drop(labels=['Tid (UTC)', 'Datum'], axis=1)
    df = df.rename(columns={df.columns[0]: 'Value'})

    # Reorganize the labels, the first label in the dataframe with dropped labels will be the "value" we are looking for
    # This is most likely a temporary step as it won't matter later on when we visualize the data as a graph
    df = df[['Year', 'Month', 'Day', 'Hour', 'Whole', df.columns[0]]]
    return df

def get_interval(df: pd.DataFrame, min_time: datetime.datetime, max_time: datetime.datetime):
    """
        Takes a dataframe, and two time periods and returns a new dataframe that contains data from the original dataframe that satisfies the time interval.
    """
    # min_day = f'{min_date.year}-{min_date.month:02d}-{min_date.day:02d}'
    # max_day = f'{max_date.year}-{max_date.month:02d}-{max_date.day:02d}'
    # min_hr = min_date.hour
    # max_hr = max_date.hour
    # A very advanced expression to finding all the rows that satisfies the given interval
    m = df.loc[(df['Whole'] >= min_time.timestamp()) & (df['Whole'] <= max_time.timestamp())]  #
    m = m.reset_index(drop=True)
    return m

df = load_data('airtemp')
min_date, max_date = datetime.datetime(2019, 12, 28), datetime.datetime(2019, 12, 28, 23)

df = get_interval(df, min_date, max_date)
print(df)