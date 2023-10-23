import requests 
import pandas as pd 
from bs4 import BeautifulSoup

api_key = 'oJpGQu7eUn5UKR6aYyB8oUy3c5bEwasj'

url = "https://api.apilayer.com/exchangerates_data/symbols"

currency_codes = ["MXN", "BRL", "HUF", "KRW", "ZAR", "NZD", "AED", "USD"]

headers = {
    "apikey": api_key
}

currency_names = {}

for code in currency_codes:
    params = {
        "symbols": code
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        if code in data.get("symbols", {}):
            currency_names[code] = data["symbols"][code]

for code, name in currency_names.items():
    print(f"{code}: {name}")

url = "https://api.apilayer.com/exchangerates_data/timeseries"

params = {
    'start_date': '2023-08-01',
    'end_date': '2023-10-08',
    'symbols': 'MXN, BRL, HUF, KRW, ZAR, NZD, AED, USD',
    'base': 'EUR'
}

headers = {
    'apikey': api_key
}

response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    data = response.json()
    
    df = pd.DataFrame(data["rates"]).T
    correlations = df.corrwith(df['USD'])

    highest_positive_corr = correlations.idxmax()
    highest_positive_corr_coeff = correlations.max()
    highest_negative_corr = correlations.idxmin()
    highest_negative_corr_coeff = correlations.min()

    print('Currency Names from (A.): MXN, BRL, HUF, KRW, ZAR, NZD, AED, USD')
    print(f'The currency with the highest postive correlation with USD: {highest_negative_corr} ({highest_positive_corr_coeff})')
    print(f'The currency with the highest negative correlation with USD: {highest_negative_corr} ({highest_negative_corr_coeff})')

    df.to_csv('currency_exchange.csv')
else: 
    print('Failed to retrieve data. Stats code:', response.status_code)

### PART 2

url = 'https://editorial.rottentomatoes.com/guide/140-essential-action-movies-to-watch-now/'

response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

titles = []
years = []
scores = []
ranks = []
categories = []

movie_list = soup.find_all('div', class_ = 'article_movie_title')

for rank, movie in enumerate(movie_list, start = 1):
    title = movie.a.text
    titles.append(title)

    year_text = movie.find('span', class_ = 'subtle').text
    year = int(year_text.strip('()'))
    years.append(year)

    score = int(movie.find('span', class_ = 'tMeterScore').text.strip('%'))
    scores.append(score)

    ranks.append(rank)

    category = movie.find('p', class_ = 'certification')
    if category:
        categories.append(category.text.strip())
    else:
        categories.append('')
    
movie_data = {
    'Title': titles,
    'Year': years,
    'Score': scores,
    'Rank': ranks,
    'Category': categories
}

df = pd.DataFrame(movie_data)

print(df.head())

mean_year = df['Year'].mean()
mean_score = df['Score'].mean()
corr_score_rank = df['Score'].corr(df['Rank'])
mean_rank_certified_fresh = df[df['Category'] == 'Certified Fresh']['Rank'].mean()
mean_rank_fresh = df[df['Category'] == 'Fresh']['Rank'].mean()
mean_rank_rotten = df[df['Category'] == 'Rotten']['Rank'].mean()


print(f"Mean year: {mean_year}\n")
print(f"Mean score: {mean_score}\n")
print(f"Correlation coefficient between score and rank: {corr_score_rank}\n")
print(f"Mean rank of 'Certified Fresh': {mean_rank_certified_fresh}\n")
print(f"Mean rank of 'Fresh': {mean_rank_fresh}\n")
print(f"Mean rank of 'Rotten': {mean_rank_rotten}\n")

#df.to_csv('action_movies.csv', index = None)

### PART 3 

url = "https://restcountries.com/v3/all"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()

    countries = []
    populations = []
    areas = []
    languages = []
    currencies = []

    for country in data:
        countries.append(country.get("name", ""))
        populations.append(country.get("population", ""))
        areas.append(country.get("area", ""))
        languages_str = country.get("languages", "")
        languages.append(languages_str)
        currencies_str = country.get("currencies", "")
        currencies.append(currencies_str)

    country_data = {
        'Country': countries,
        'Population': populations,
        'Area': areas,
        'Languages': languages,
        'Currencies': currencies
    }

    df = pd.DataFrame(country_data)

    df.to_csv('my_api_data.csv', index = None)
else:
    print(f'Failed to retrieve data. Status code: {response.status_code}')



