import requests as req
import re
from bs4 import BeautifulSoup
import matplotlib

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
    count_link = 1  # count link in 'links'
    auto = {}  # storage for saving data auto

    for link in links:
        html_car = req.get('https://www.olx.ua' + link.get('href')).text
        soup = BeautifulSoup(html_car, 'lxml')
        data = {
            'Release date': '',
            'Price': ''
        }

        for d in soup.find_all('p', class_='css-xl6fe0-Text eu5v0x0'):
            if re.search(r'Рік випуску: .*', d.text):
                data['Release date'] = re.search(r'\d\d\d\d', d.text).group(0)

        if soup.find('h3', class_='css-okktvh-Text eu5v0x0').text is not None:
            data['Price'] = soup.find('h3', class_='css-okktvh-Text eu5v0x0').text
        else:
            data['Price'] = '-'

        auto[count_link] = data
        count_link = count_link + 1
    return auto


def gistograme(data: dict):
    x = set()
    for d in data.keys():
        x.add(int(data[d]['Release date']))
    print(x)


autos = data_parsing(get_html(URL))
# print(autos)
gistograme(autos)


