
import random
import time
from io import BytesIO
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

BASE_URL = 'https://www.metal-archives.com'
BANDS_GENRE_ENDPOINT = 'browse/ajax-genre/g/'
BANDS_GENRE_TAIL = '/json/1'
BAND_ENDPOINT = '/band/view/id'
LOGO_ENDPOINT = 'images/'
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


def _metallum_request(endpoint=None, url=None, id=None, tail=None, params=None):

    if not id:
        id = ''
    if not tail:
        tail = ''
    if not url:
        url = urljoin(BASE_URL, url=f'{endpoint}{id}{tail}')

    timeout_count = 0

    while timeout_count < 5:  # Loop 10 times before quitting
        try:
            r = requests.get(url, headers=HEADER, params=params)
            r.raise_for_status()
            return r
        except requests.exceptions.HTTPError as errh:
            timeout_count += 1
            err_msg = f'{errh}. Retrying attempt {timeout_count} of 5.'
            tqdm.write(err_msg)
            time.sleep(random.uniform(3.0, 4.0))  # Wait between 3 and 4 seconds before resuming
            r = None
        except requests.exceptions.ConnectionError as errc:
            tqdm.write('Connection failed.')
            r = None

    return r


def get_metallum_bands(genre, payload):

    data_page = []

    r = _metallum_request(endpoint=BANDS_GENRE_ENDPOINT, id=genre, tail=BANDS_GENRE_TAIL, params=payload)
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


def get_logo_url(band_url):

    r = _metallum_request(url=band_url)
    try:
        soup = BeautifulSoup(r.content, 'lxml')
        logo_link = soup.find('a', {'id': 'logo'})
        logo_url = logo_link['href']
    except AttributeError:
        logo_url = None
    except TypeError:
        logo_url = None

    return logo_url


def get_logo(logo_url):

    r = _metallum_request(logo_url)
    try:
        logo_bytes = BytesIO(r.content)
    except AttributeError:
        logo_bytes = None
    except OSError:
        logo_bytes = None

    return logo_bytes
