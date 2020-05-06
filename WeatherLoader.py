import pandas as pd

CSV_SEPARATOR = ';'

WEATHER_DATA_PATH = './weatherdata'
WEATHER_PAIRS = {
    'airtemp': 'airtemp.csv',
    'precip': 'precip.csv'
}

def load_data(data):
    path = f'{WEATHER_DATA_PATH}/{WEATHER_PAIRS[data]}'
    df = pd.read_csv(path, sep=CSV_SEPARATOR)
    return df

df = load_data('precip')
print(df.head())