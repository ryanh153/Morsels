import requests
import csv


gist_url = 'https://gist.githubusercontent.com/reuven/77edbb0292901f35019f17edb9794358/raw/2bf258763cdddd704f8ffd3ea9a3e81d25e2c6f6/cities.json'
KEYS = ['city', 'state', 'rank', 'population']


def cities_to_csv(url, filename):
    with open(filename, 'w+') as of:
        dw = csv.DictWriter(of, fieldnames=KEYS, delimiter='\t', extrasaction='ignore')
        dw.writerows(requests.get(url).json())
