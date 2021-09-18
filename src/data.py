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


def save_png_image(image, output):

    msg = 'Failed to save/convert'
    try:
        image = image.convert('L')
        image.save(output, 'PNG')
        msg = 'Successfully saved'
    except OSError as erro:
        msg = f'{msg} ({erro})'
    except UnidentifiedImageError as erru:
        msg = f'{msg} ({erru})'

    return msg


def read_tarfile_contents(filepath):

    image_list = []
    tar = tarfile.open(filepath, 'r:gz')
    members = tar.getmembers()
    for member in members:
        id = member.name
        image_list.append(id.strip('.png'))
    return image_list


def make_tarfile(tarfilename, dir):

    with tarfile.open(tarfilename, 'W:gz') as tar:
        tar.add(dir, arcname=os.path)


def extract_from_tarfile(tarfilepath, id, outfilepath):
    filename = f'{id}.png'
    with tarfile.open(tarfilepath, 'r:gz') as tar:
        tar.extract(filename, path=outfilepath)
