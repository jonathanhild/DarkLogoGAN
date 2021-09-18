import os
import csv
import tarfile

from PIL import Image, UnidentifiedImageError


def to_csv(data, filename):

    keys = data[0].keys()
    with open(filename, mode='w') as csvfile:
        dict_writer = csv.DictWriter(csvfile, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)


def from_csv(filename):

    with open(filename, mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        band_data = list(reader)
        return band_data


def save_png_image(content, output):

    save_msg = 'Failed to save/convert'
    try:
        image = Image.open(content).convert('L')
        image.save(output, 'PNG')
        save_msg = 'Successfully saved'
    except OSError as erro:
        save_msg = f'{save_msg} ({erro})'
    except UnidentifiedImageError as erru:
        save_msg = f'{save_msg} ({erru})'

    return save_msg


def make_logo_tarfile(output_filename, source_dir):

    with tarfile.open(output_filename, 'W:gz') as tar:
        tar.add(source_dir, arcname=os.path)


def extract_logo_tarfile(tar_filename, output_dir):

    tar = tarfile.open(tar_filename)
    tar.extractall(output_dir)
    tar.close()
