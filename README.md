# DarkLogoGAN

A generative deep learning model for creating black metal and death metal logos.

## Data

### band_data

- `id`: www.metal-archives.com band ID.
- `url`: The URL for the band page; where the logo image was obtained.
- `name`: The band's name.
- `country`: The band's country of origin.
- `genre`: The main genre (black or death) that is associated with the band. Band's genres may be transitory and can be associated with both.
- `full_genre`: The full (list of) genres associated with the band.
- `status`: The activity status of the band.

The dataset is made up of 93,044 bands (as of September 5, 2021).

### Images

The imageset is made up of 80-90K PNG images in 8-bit black and white. Images are names with the band ID.

## GAN Model

{{To Be Added}}

## Working with `darklogo.py`

### Downloading the dataset

```bash
python darklogo.py bands --output data/
```

```bash
python darklogo.py logos --input data/band_data.csv --output data/images/
```

### Training The Model

```bash
python darklogo.py train --input data/images/
```

### Creating Logos

```bash
python darklogo.py generate --name "Band Name" --output logos/
```

## examples

