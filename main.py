from bs4 import BeautifulSoup
import requests as req
import re
import matplotlib.pyplot as plt
import numpy as np

URL = 'https://www.olx.ua/d/uk/transport/legkovye-avtomobili/bmw' \
      '/?currency=UAH&search%5Bfilter_enum_model%5D%5B0%5D=7-series '


# function for getting html page
def get_html(url):
    resp = req.get(url).text
    return resp


# function for extract data from html page
def data_parsing(data_page):
    soup = BeautifulSoup(data_page, 'lxml')
    links = list(soup.find_all('a', class_='css-1bbgabe'))  # storage for saving links
    auto = []  # storage for saving data auto

    for link in links:
        html_car = req.get('https://www.olx.ua' + link.get('href')).text
        soup = BeautifulSoup(html_car, 'lxml')
        price_tag = soup.find('h3', class_='css-okktvh-Text eu5v0x0')

        if price_tag is not None and re.search(r'\d', price_tag.text) is not None:
            data = {'Release date': '', 'Price': price_tag.text}

            for d in soup.find_all('p', class_='css-xl6fe0-Text eu5v0x0'):
                if re.search(r'Рік випуску: .*', d.text):
                    data['Release date'] = re.search(r'\d\d\d\d', d.text).group(0)

            auto.append(data)
    return auto


# function for painting analytic gistogram
def gistograme(data: list):
    dates = set(int(v['Release date']) for v in data)
    price = dict.fromkeys(dates)

    for k in price.keys():
        price[k] = []

    for value in data:

        if '$' in value['Price'] or '€' in value['Price']:
            price[int(value['Release date'])].append(int(re.search(r'\d+', value['Price'].replace(' ', '')).group()))
        else:
            price[int(value['Release date'])].append(
                int(re.search(r'\d+', value['Price'].replace(' ', '')).group()) / 37)

    for key, value in price.items():
        price[key] = int(np.average(value))

    plt.bar(price.keys(), price.values())
    plt.show()

autos = data_parsing(get_html(URL))
gistograme(autos)
