import requests
import pandas as pd

base_url = "https://www.basketball-reference.com/draft/NBA_{year}.html"
years = range(1980, 2011)
all_players = []

# repetition for 30 years(1980~2010)
for year in years:
    
    url = base_url.format(year=year)
    response = requests.get(url)

    