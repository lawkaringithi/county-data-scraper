import json
import logging
import sys

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

logging.basicConfig(format='%(asctime)s : %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

base_url = 'https://en.wikipedia.org'


def scrap_constituency_data(url):
    """
    scraps constituency data from the url and returns a list of constituency wards

    :param url: the url to scrap county data from
    :return:
    """

    ward_data = []

    r = requests.get(url)
    if not r.ok:
        logger.error(f'failed to scrap {url} : {r.text}')
        return ward_data

    s = BeautifulSoup(r.text, 'html.parser')

    tables = s.find_all('table', {'class': 'wikitable'})
    for table in tables:
        title = table.tbody.tr.text.strip()

        if title != 'Wards':
            continue

        for tr in table.find_all('tr')[1:]:
            ward = tr.td.text.strip() if tr.td else ''
            if not ward:
                continue

            if ward == 'Total':
                break

            ward_data.append(ward)

    return ward_data


if __name__ == '__main__':
    res = requests.get(f'{base_url}/wiki/List_of_constituencies_of_Kenya')
    if not res.ok:
        logger.error(res.text)
        sys.exit(1)

    soup = BeautifulSoup(res.text, 'html.parser')

    # collect county data
    county_data = []
    for element in soup.find_all('h4'):
        county_span = element.find('span', {'class': 'mw-headline'})

        if county_span.a.get('title').endswith('County'):
            county_name = county_span.a.text.rstrip('County')
            county_url = county_span.a.get('href')

            # create county data object
            data = {'county': county_name, 'url': f'{base_url}{county_url}'}
            county_data.append(data)

    # collect constituency data
    counter = 0
    for ul in soup.find_all('ul'):
        if not ul.li or 'Population' not in ul.li.text:
            continue

        county_index = counter

        constituencies = []
        for a in ul.find_all('a'):
            if a.get('title', '').endswith('Constituency'):
                constituencies.append({
                    'constituency': a.text,
                    'url': f'{base_url}{a["href"]}',
                    'wards': [],
                })

        county_data[county_index]['constituencies'] = constituencies
        counter += 1

    for county in tqdm(county_data):
        constituencies = county.get('constituencies', [])

        # some constituencies do not have populated wards on Wikipedia
        # they'll be blank
        for constituency in constituencies:
            retrieved_data = scrap_constituency_data(url=constituency.get('url'))
            constituency['wards'] = retrieved_data

    # write county data to file
    with open('county.json', 'w') as county_file:
        dump = json.dumps(county_data)
        county_file.write(dump)

    logger.info("The END!")
