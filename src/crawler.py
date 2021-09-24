import io
from PIL import Image

import requests
from bs4 import BeautifulSoup

HEADER = {'User-Agent': 'Mozilla/5.0 Gecko/20100101 Firefox/90.0'}
I_DISPLAY_LENGTH = 500
BAND_ENDPOINT = '/band/view/id'


def _extract_id(url: str):

    url_slices = url.split('/')
    url_slices.reverse()
    for slice in url_slices:
        if slice.isnumeric():
            return int(slice)
        else:
            continue

    return None


class MetallumBands():

    def __init__(self):

        self.bands = []
        self.s_echo = 1
        self.start = 0
        self.end = I_DISPLAY_LENGTH
        self.total = 999_999
        self.bad_request_count = 0

        if not self.bands:
            pass

    def _parse_band(self, band, genre: str):

        band_dict = {}

        href = BeautifulSoup(band[0], 'lxml')
        band_dict['id'] = _extract_id(href.a['href'])
        band_dict['url'] = href.a['href']
        band_dict['name'] = href.a.text
        band_dict['country'] = band[1]
        band_dict['genre'] = genre
        band_dict['full_genre'] = band[2]
        status = BeautifulSoup(band[3], 'lxml')
        band_dict['status'] = status.span.text

        return band_dict

    def crawl_bands(self, genre: str):

        if self.start >= self.total:  # Check if any more band records to retrieve
            msg = 'No more records to retrieve.'
        else:
            # Construct URL with genre
            url = 'https://www.metal-archives.com/browse/ajax-genre/g/' + genre + '/json/1'

            # Construct the payload with current state
            payload = dict(
                sEcho=self.s_echo,
                iDisplayStart=self.start,
                iDisplayLength=I_DISPLAY_LENGTH
            )

            try:
                r = requests.get(url, headers=HEADER, params=payload)
                r.raise_for_status()
                self.bad_request_count = 0

                json = r.json()
                self.total = json['iTotalRecords']
                raw_data = json['aaData']

                for rec in raw_data:
                    self.bands.append(self._parse_band(band=rec, genre=genre))

                msg = f'Retrieving bands {self.start + 1} to {self.end} in {genre.title()} Metal.'

                self.start += I_DISPLAY_LENGTH
                if (self.start + I_DISPLAY_LENGTH) > self.total:
                    self.end = self.total
                else:
                    self.end = self.start + I_DISPLAY_LENGTH
            except requests.exceptions.HTTPError as err_h:
                msg = f'{err_h}. Retrying with attempt {self.bad_request_count + 1}'
                self.bad_request_count += 1
            except requests.exceptions.ConnectionError as err_c:
                msg = f'{err_c}. Connection Failed.'
                self.bad_request_count += 5

        r.close()

        return msg

    def keep_crawling(self):

        return self.start <= self.total


class MetallumLogo():

    def __init__(self, band_id):
        self.msg = str()
        self.band_id = band_id
        self.logo_url = self._scrape_logo_url()
        if self.logo_url:
            self.image = self._scrape_logo()
        else:
            self.image = None

    def _parse_logo_url(self, content):

        try:
            soup = BeautifulSoup(content, 'lxml')
            logo_html = soup.find('a', {'id': 'logo'})
            logo_url = logo_html['href']
        except TypeError:
            self.msg = 'No logo URL found'
            logo_url = None

        return logo_url

    def _scrape_logo_url(self):
        url = 'https://www.metal-archives.com/band/view/id/' + self.band_id

        try:
            r = requests.get(url, headers=HEADER)
            r.raise_for_status()

            logo_url = self._parse_logo_url(r.content)
            self.msg = "Found logo"

        except requests.exceptions.HTTPError as err_h:
            self.msg = f'{err_h}'
        except requests.exceptions.ConnectionError as err_c:
            self.msg = f'{err_c}'

        r.close()

        return logo_url

    def _scrape_logo(self):

        image = None

        try:
            r = requests.get(self.logo_url)
            r.raise_for_status()
            image_bytes = io.BytesIO(r.content)
            image = Image.open(image_bytes)

        except requests.exceptions.HTTPError as err_h:
            self.msg = f'{err_h}'
        except requests.exceptions.ConnectionError as err_c:
            self.msg = f'{err_c}'

        r.close()

        return image
