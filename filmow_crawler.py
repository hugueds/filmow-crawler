import requests
from bs4 import BeautifulSoup
import itertools
import csv
import re

ITEMS_PER_PAGE = 24
MAX_MOVIES_PAGE = 0
MAX_SERIES_PAGE = 9

current_page = 1

user = 'hugueds'
media_type = 'series'
watch_type = 'ja-vi'

categories = ['all', 'filmes', 'series', 'quero-ver', 'ja-vi']

BASE_URL = 'https://filmow.com/usuario/{user}/{media_type}/{watch-type}'

url = BASE_URL
url = url.replace('{user}', user)
url = url.replace('/{watch-type}', f'/{watch_type}')
url = url.replace('/{media_type}', f'/{media_type}')

global_movies_list = []


def get_film(url, page):
    movies_list = []
    page_url = f'{url}?pagina={page}'
    print(f'Searching for Page {page_url}')
    result = requests.get(page_url)    
    soup = BeautifulSoup(result.content, 'html.parser')
    html_movies_list = soup.find(id='movies-list')
    for _li in html_movies_list.find_all('li'):
        movie_name = _li.find('span', { "class": "wrapper"}).a.img['alt']
        movies_list.append(movie_name)
    return movies_list

def get_original_title(movie_name):
    p = re.compile('(^.+)\((.+)\)')
    portuguese = p.search(movie_name).group(1)
    original = p.search(movie_name).group(2)
    return [portuguese, original]

def get_season(series_name):
    p = re.compile('(^.+)\s\((.+)\)\s\((.+)\)')
    try:
        name = p.search(series_name).group(1)
        season = p.search(series_name).group(2)
        original = p.search(series_name).group(3)
        return [name, season, original]
    except:
        return [series_name, '' ,series_name]


def save_list(movies_list):
    with open(f'csv_{watch_type}_{media_type}.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(movies_list)
    

for i in range(1, MAX_MOVIES_PAGE + 1):
    movies = get_film(url, i)    
    global_movies_list.append(movies)

flatten_list = list(itertools.chain(*global_movies_list))
upper_list = list(map(lambda x: get_original_title(x), flatten_list))    
 

url = BASE_URL
url = url.replace('{user}', user)
url = url.replace('/{watch-type}', f'/{watch_type}')
url = url.replace('/{media_type}', f'/{media_type}')

global_movies_list = []

for i in range(1, MAX_SERIES_PAGE + 1):
    movies = get_film(url, i)    
    global_movies_list.append(movies)

flatten_list = list(itertools.chain(*global_movies_list))
upper_list = list(map(lambda x: get_season(x), flatten_list))

save_list(upper_list)





