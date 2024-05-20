import requests
from bs4 import BeautifulSoup
import csv

url_main = 'https://www.lego.com'
url_themes = 'https://www.lego.com/en-us/themes'


def get_soup(url, page=1):
    if page == 1:
        r = requests.get(url=url)
    else:
        url = f'{url}?page={page}&offset=0'
        r = requests.get(url=url)
    return BeautifulSoup(r.text, 'lxml')


def get_themes(soup):
    themes = soup.find('section').ul
    themes = themes.find_all('li')

    themes_list = []

    for theme in themes:
        theme_dict = {
            'name': theme.h2.span.text,
            'url': f'{url_main}{theme.a.get("href")}',
        }
        themes_list.append(theme_dict)

    keys = themes_list[0].keys()

    with open('themes.csv', 'w', newline='') as f:
        dict_writer = csv.DictWriter(f, keys,)
        dict_writer.writeheader()
        dict_writer.writerows(themes_list)

    return themes_list


def get_toys_pages(soup):
    num_toys = int(soup.select('span[data-value]')[0].get('data-value'))
    num_pages = num_toys // 18 + 1

    return num_toys, num_pages


def main():
    # soup = get_soup(url=url_themes)
    # themes = get_themes(soup=soup)
    soup = get_soup(url='https://www.lego.com/en-us/themes/city')
    print(get_toys_pages(soup=soup))


if __name__ == '__main__':
    main()
