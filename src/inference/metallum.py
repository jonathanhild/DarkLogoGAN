
import random
import time
from io import BytesIO
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

BASE_URL = 'https://www.metal-archives.com'
HEADER = {'User-Agent': 'Mozilla/5.0 Gecko/20100101 Firefox/90.0'}


def _extract_band_id(url):

    url_parts = url.split('/')
    url_parts.reverse()
    for part in url_parts:
        if part.isnumeric():
            return int(part)
        else:
            try:
                raise TypeError
            except TypeError as e:
                print(e)
    return None


def metallum_request(timeout_count, endpoint=None, url=None, id=None, tail=None, params=None):

    if not id:
        id = ''
    if not tail:
        tail = ''
    if not url:
        url = urljoin(BASE_URL, url=f'{endpoint}{id}{tail}')

    err_msg = None

    try:
        r = requests.get(url, headers=HEADER, params=params)
        r.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        err_msg = f'{errh}. Retrying attempt {timeout_count} of 5.'
        time.sleep(random.uniform(3.0, 4.0))  # Wait between 3 and 4 seconds before resuming
        r = None
    except requests.exceptions.ConnectionError as errc:
        err_msg = 'Connection failed.'
        r = None

    return r, err_msg


def get_metallum_bands(r, genre, payload):

    data_page = []

    json = r.json()

    total_records = json['iTotalRecords']

    for aa in json['aaData']:
        band_dict = {}
        href = BeautifulSoup(aa[0], 'lxml')
        band_dict['id'] = _extract_band_id(href.a['href'])
        band_dict['url'] = href.a['href']
        band_dict['name'] = href.a.text
        band_dict['country'] = aa[1]
        band_dict['genre'] = genre
        band_dict['full_genre'] = aa[2]
        status = BeautifulSoup(aa[3], 'lxml')
        band_dict['status'] = status.span.text

        data_page.append(band_dict)

    return payload, total_records, data_page


def get_logo_url(r):

    try:
        soup = BeautifulSoup(r.content, 'lxml')
        logo_link = soup.find('a', {'id': 'logo'})
        logo_url = logo_link['href']
    except AttributeError:
        logo_url = None
    except TypeError:
        logo_url = None

    return logo_url


def get_logo(r):

    try:
        logo_bytes = BytesIO(r.content)
    except AttributeError:
        logo_bytes = None
    except OSError:
        logo_bytes = None

    return logo_bytes
