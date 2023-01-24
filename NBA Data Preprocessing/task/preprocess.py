import pandas as pd
import os
import requests

# Checking ../Data directory presence
if not os.path.exists('../Data'):
    os.mkdir('../Data')

# Download data if it is unavailable.
if 'nba2k-full.csv' not in os.listdir('../Data'):
    print('Train dataset loading.')
    url = "https://www.dropbox.com/s/wmgqf23ugn9sr3b/nba2k-full.csv?dl=1"
    r = requests.get(url, allow_redirects=True)
    open('../Data/nba2k-full.csv', 'wb').write(r.content)
    print('Loaded.')

data_path = "../Data/nba2k-full.csv"


# write your code here
def clean_data(d):
    d = pd.read_csv(d)

    def category(x):
        if x == "USA":
            return "USA"
        return "Not-USA"

    d['b_day'] = pd.to_datetime(d['b_day'], format='%m/%d/%y')
    d['draft_year'] = pd.to_datetime(d['draft_year'], format='%Y' )
    d['team'].fillna('No Team', inplace=True)
    d['height'] = d['height'].apply(lambda x: x.split('/')[1])
    d['weight'] = d['weight'].apply(lambda x: x.split('/')[1].rstrip(' kg. '))
    d['salary'] = d['salary'].apply(lambda x: x[1:])
    d[['height', 'weight', 'salary']] = d[['height', 'weight', 'salary']].astype('float')
    d['country'] = d['country'].map(category)
    d['draft_round'].replace('Undrafted', '0', inplace=True)

    return d


def feature_data(data):
    if not data.empty:
        data.version = data['version'].map(lambda x: (2020 if x[-2:] == 20 else 2021))
        data['version'] = pd.to_datetime(data['version'], format='%Y' )
        data['age'] = (data['version'] - data['b_day']).astype('timedelta64[Y]')
        data['experience'] = data['version'].dt.year - data['draft_year'].dt.year - 1
        data['bmi'] = data['weight'] / data['height'] ** 2
        data.drop(columns=['version','b_day', 'draft_year', 'weight', 'height', ], inplace=True)

        cols = []
        for col in data.columns:
            if data[col].dtype == "object":
                cols.append(col)
        data.drop(data.loc[:, cols].loc[:, data.nunique() > 50], axis=1, inplace=True)
        return data

def multicol_data(df):
    cols = df.describe().columns
    corrs = df[cols].corr()
    numeric_cols = list(set(corrs.columns) - set(["salary"]))
    to_drop = list()
    for i in range(num_cols := len(numeric_cols)):
        for j in range(i + 1, num_cols):
            if abs(corrs[numeric_cols[i]][numeric_cols[j]]) >= 0.5:
                if corrs["salary"][numeric_cols[i]] > corrs["salary"][numeric_cols[j]]:
                    to_drop.append(numeric_cols[j])
                else:
                    to_drop.append(numeric_cols[i])

    return df.drop(to_drop, axis=1)