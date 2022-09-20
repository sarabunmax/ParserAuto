from bs4 import BeautifulSoup
import csv
import matplotlib.pyplot as plt
import UserConfig as UC
import numpy as np
import re
import requests as req
import time


# function for getting html page
def get_html(url):
    resp = req.get(url)

    # block for cheking http responce
    if resp.status_code != 200:
        time.sleep(1)
        resp = req.get(url)  # additional connection attempt
        if resp.status_code != 200:
            raise ConnectionError()
        else:
            return resp.text
    else:
        return resp.text


# function for extract data from html page
def html_parsing(html_page, data_stoarage: list):
    soup = BeautifulSoup(html_page, 'lxml')
    links = list(soup.find_all('a', class_='css-1bbgabe'))  # storage for saving links to car page

    #  handlig each page
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


#  function for writing clean data to csv format
def write_data(data: list, config: UC.Config):
    csv_file = f'{config.direction}\\vechicle_data.csv'
    with open(csv_file, 'w', newline='') as file:
        writer = csv.DictWriter(f=file, fieldnames=['Release date', 'Price'], dialect='excel')
        writer.writerow({'Release date': 'Release date', 'Price': 'Price'})
        for d in data:
            writer.writerow(d)


# function for painting analytic gistogram
def gistograme(data: list, config: UC.Config):
    dates = set(int(v['Release date']) for v in data)  # Available dates
    price = dict.fromkeys(dates)  # initialization dictionary with keys

    # assigning a list to each key
    for k in price.keys():
        price[k] = []

    # filling dictionary
    for value in data:

        if '$' in value['Price'] or '€' in value['Price']:
            price[int(value['Release date'])].append(int(re.search(r'\d+', value['Price'].replace(' ', '')).group()))
        else:
            price[int(value['Release date'])].append(
                int(re.search(r'\d+', value['Price'].replace(' ', '')).group()) / 37)

    # calculate average value price
    for key, value in price.items():
        price[key] = int(np.average(value))

    # building and saving plot
    plt.bar(price.keys(), price.values())
    plt.title('Price analytic')
    plt.xlabel('Vehicle release date')
    plt.ylabel('Average price $')
    plt.savefig(f'{config.direction}\\AveragePrice.png')

