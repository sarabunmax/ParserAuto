from bs4 import BeautifulSoup
import requests as req
import re
import matplotlib.pyplot as plt
import numpy as np

URL = 'https://www.olx.ua/d/uk/transport/legkovye-avtomobili/bmw' \
      '/?currency=UAH&search%5Bfilter_enum_model%5D%5B0%5D=7-series'


# function for getting html page
def get_html(url):
    resp = req.get(url).text
    return resp


# function for extract data from html page
def html_parsing(html_page, data_stoarage: list):
    soup = BeautifulSoup(html_page, 'lxml')
    links = list(soup.find_all('a', class_='css-1bbgabe'))  # storage for saving links

    for link in links:
        html_car = req.get('https://www.olx.ua' + link.get('href')).text
        soup = BeautifulSoup(html_car, 'lxml')
        price_tag = soup.find('h3', class_='css-okktvh-Text eu5v0x0')

        if price_tag is not None and re.search(r'\d', price_tag.text) is not None:
            data = {'Release date': '', 'Price': price_tag.text}

            for d in soup.find_all('p', class_='css-xl6fe0-Text eu5v0x0'):
                if re.search(r'Рік випуску: .*', d.text):
                    data['Release date'] = re.search(r'\d\d\d\d', d.text).group(0)

            data_stoarage.append(data)


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
    # print(price)
    # for key, value in price.items():
    #     price[key] = int(np.average(value))
    #
    # plt.bar(price.keys(), price.values())
    # plt.show()


page_numb = 1
autos_info = []
last_size = 1
# html_parsing(get_html(f'{URL}&page={page_numb}'), autos_info)

while True:

    if len(autos_info) != last_size:
        last_size = len(autos_info)
        html_parsing(get_html(f'{URL}&page={page_numb}'), autos_info)
        page_numb += 1
    else:
        break

print(len(autos_info))
#gistograme(autos_info)