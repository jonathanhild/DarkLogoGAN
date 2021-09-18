# Copyright 2021 jonathan.
# SPDX-License-Identifier: GPL-2.0-only

import os

import click
from tqdm import tqdm

from src.inference.data import from_csv, save_png_image, to_csv
from src.inference.metallum import metallum_request, get_logo, get_logo_url, get_metallum_bands

GENRES = ['black', 'death']
BANDS_GENRE_ENDPOINT = 'browse/ajax-genre/g/'
BANDS_GENRE_TAIL = '/json/1'
BAND_ENDPOINT = '/band/view/id'
LOGO_ENDPOINT = 'images/'


@click.group()
def main():
    """Pass-through function for click command groups."""
    pass


@main.command()
@click.option('--output', '-o', help='Relative path and filename for band data csv')
def bands(output=None):

    if not output:
        output = os.path.join('data', 'band_data.csv')

    band_data = []

    for genre in GENRES:
        total_records = 999_999  # Large default value to allow for request initialization.
        payload = {
            'sEcho': 1,
            'iDisplayStart': 0,
            'iDisplayLength': 500
        }

        pbar = tqdm(total=total_records)
        pbar.total = total_records

        while payload['iDisplayStart'] < total_records:

            bands_from = payload['iDisplayStart'] + 1
            if (payload['iDisplayStart'] + payload['iDisplayLength']) > total_records:
                bands_to = total_records
            else:
                bands_to = payload['iDisplayStart'] + payload['iDisplayLength']
            pbar.desc = f"Fetching bands {bands_from} to {bands_to} for genre '{genre}'"

            for counter in range(5):
                r, err_msg = metallum_request(
                    timeout_count=counter, endpoint=BANDS_GENRE_ENDPOINT,
                    id=genre, tail=BANDS_GENRE_TAIL, params=payload
                )
                if err_msg:
                    tqdm.write(err_msg)
                    continue
                else:
                    break

            payload, total_records, data_page = get_metallum_bands(r, genre, payload)
            band_data += data_page
            pbar.total = total_records

            payload['iDisplayStart'] += len(data_page)

            pbar.update(len(data_page))

            # Save band data to csv file
            to_csv(band_data, output)


@main.command()
@click.option('--infile', '-i', help='Input CSV file of band data. Defaults to ./data/band_data.csv')
@click.option('--outdir', '-o', help='Output directory to save logo images. Defaults to ./data/images/')
def logos(infile=None, outdir=None):

    if not infile:
        infile = os.path.join('data', 'band_data.csv')
    if not outdir:
        outdir = os.path.join('data', 'images')

    band_data = from_csv(infile)

    image_list = [image.strip('.png') for image in os.listdir(outdir)]

    pbar = tqdm(band_data)

    for band in pbar:

        logo_url = None
        logo = None
        # Check if logo image is present in the outdir directory.
        if (band['id'] in image_list):
            tqdm.write(f"Logo already exists for {band['name']} (id: {band['id']}). Skipping.")
            band['logo_status'] = 'downloaded'
            continue

        pbar.desc = f"Getting logo for {band['name']} (id: {band['id']})"

        for counter in range(5):
            r, err_msg = metallum_request(timeout_count=counter, url=band['url'])
            if err_msg:
                tqdm.write(err_msg)
                continue
            else:
                break

        logo_url = get_logo_url(r)

        if logo_url:
            for counter in range(5):
                r, err_msg = metallum_request(timeout_count=counter, url=logo_url)
                logo = get_logo(r)
                if err_msg:
                    tqdm.write(err_msg)
                    continue
                else:
                    break
        else:
            continue

        if logo:
            filename = band['id'] + '.png'
            filepath = os.path.join(outdir, filename)
            save_msg = save_png_image(logo, filepath)
            band['logo_status'] = 'downloaded'
            tqdm.write(f"{save_msg} {filepath} for {band['name']} (id: {band['id']})")
            image_list.append(band['id'])
        else:
            tqdm.write(f"No logo found for {band['name']} (id: {band['id']}). Skipping.")
            band['logo_status'] = 'no logo'
            continue

    tqdm.write(f'Complete download of {len(image_list)}.')

    to_csv(band_data, infile)


if __name__ == '__main__':
    main()
