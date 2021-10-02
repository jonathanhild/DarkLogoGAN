# DarkLogoGAN

A generative deep learning model for creating black metal and death metal logos.

## Metal Archives

<div align="center">
    <h1>Exploratory data analysis of band data</h1>
    <img src="https://www.metal-archives.com/css/default/images/smallerlogo.jpg">
</div>

MA is the foremost source for data on heavy metal music on the interent. The site collects data on bands, albums, lyrics, band members, photos and logos, user reviews, and much more. MA is similar to Wikipedia 

For some thing more, MA shows it's depth of data from their statistics page here: [www.metal-archives.com/stats](https://www.metal-archives.com/stats).


## Data Sources

### metal_data

`metal_data` is made up of metadata related to the imageset. The field include:

- `id`: www.metal-archives.com band ID.
- `url`: The URL for the band page; where the logo image was obtained.
- `name`: The band's name.
- `country`: The band's country of origin.
- `genre`: The main genre (black or death) that is associated with the band. Band's genres may be fluid and bands occasionally will be labeled with both.
- `full_genre`: The full (list of) genres associated with the band.
- `status`: The activity status of the band.

### Images

The imageset is made up of 80-90K PNG images in 8-bit black and white. Images are names with the band ID.

## Generative Models

{{to be added}}

## Working with `darklogo.py`

### Downloading the dataset

```bash
>>>python darklogo.py bands --genre black
```

```bash
>>>python darklogo.py logos --tarfile ./data/logos.tar.gz
```

### Processing Images

```bash
>>>python 
```

### Training The Model

```bash
>>>python darklogo.py train --input data/images/
```

### Creating Logos

```bash
>>>python darklogo.py generate --name [name] --output logos/
```

## Examples of Generated Logos

{{to be added}}

## Status

- (Current): EDA notebooks and image pre-processing code.
- 9/18/21: web crawler. Downloaded data and imageset.
