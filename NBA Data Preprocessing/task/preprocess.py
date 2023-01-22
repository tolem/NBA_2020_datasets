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

