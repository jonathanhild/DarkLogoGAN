import glob
import os
from datetime import datetime

import click
from tqdm import tqdm

from src.crawler import MetallumBands, MetallumLogo
from src.data import (from_csv, make_tarfile, open_tarfile, read_tarfile_contents,
                      save_png_image, to_csv)


@click.group()
def main():
    """Pass-through function for click command groups."""
    pass


@main.command()
@click.option('--genre', '-g', help="Specify the heavy metal genre: 'black' or 'death'")
def bands(genre):

    start = datetime.now()

    file_time = start.strftime('%y%m%d')
    filename = f'{genre}_metal_data_{file_time}.csv'
    filepath = os.path.join('data', filename)

    bands = MetallumBands()

    pbar = tqdm(bands.total, dynamic_ncols=True)

    while bands.keep_crawling():
        msg = bands.crawl_bands(genre)
        pbar.total = bands.total
        pbar.desc = msg
        pbar.update(bands.end - bands.start)
        # Incrementally save band data to csv file
        to_csv(bands.bands, filepath)

    pbar.close()
    runtime = str(datetime.now() - start)
    tqdm.write(f'Crawling finished in {runtime} for {genre.title()} Metal. {bands.total} saved to {filepath}.')


@main.command()
@click.option('--tarpath', '-t',
              help='The file path of a tar file with logo images. Save time in downloading existing images.')
def logos(tarpath):

    band_data = []
    existing_images = []

    data_dir = 'data'
    inpath = os.path.join(data_dir, '*.csv')
    if not tarpath:
        tarpath = os.path.join('data', 'logos.tar.gz')
    infiles = glob.glob(inpath)
    for file in infiles:
        data = from_csv(file)
        band_data += data

    if os.path.exists(tarpath):
        tar = open_tarfile(tarpath)
        tqdm.write(f'Reading list of images from {tarpath}.')
        existing_images = read_tarfile_contents(tarpath)
        tqdm.write('Complete. Starting logo crawler.')
    else:
        tar = make_tarfile(tarpath)
        tqdm.write('No tar archive found. Starting logo crawler.')

    pbar = tqdm(band_data, dynamic_ncols=True)

    for band in pbar:
        id = band['id']
        name = band['name']
        band_msg = f'{name} (id: {id})'
        if id in existing_images:
            tqdm.write(f'Image already downloaded/archived for {band_msg}.')
            continue
        else:
            pbar.desc = f'Searching for logo for {band_msg}.'
            logo = MetallumLogo(band_id=id)
            img_msg = logo.msg
            if logo.image:
                filename = f'{id}.png'
                filepath = os.path.join(data_dir, filename)
                save_msg = save_png_image(logo.image, filepath)
                tar.add(filepath, arcname=filename)
                os.remove(filepath)
                tqdm.write(f'{img_msg} {filename} for {band_msg}. {save_msg}.')

    tar.close()


if __name__ == '__main__':
    main()
