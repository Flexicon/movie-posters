from settings import log, API_KEY, MOVIE_API

import requests
import csv
import re


def get_poster_for_title(title):
    """Returns a string path to the poster image for a given title"""
    # remove unneccasry brackets from title
    title = re.sub(r'\(.*?\)', '', title)
    log.info('Search for movies by title: {}...'.format(title))
    res = MOVIE_API.search(title)
    log.info('Found {} movies...'.format(len(res)))
    poster = None

    for movie in res:
        if movie.poster_path:
            poster = movie.poster_path
            break

    log.info('Poster: {}'.format(poster))
    return poster


def get_image_base_url(api_key):
    """Returns base image url string
    along with an image size retrieved
    from the configuration API
    """
    example_sizes = ['w342', 'w185', 'w154']
    url = 'https://api.themoviedb.org/3/configuration'
    payload = {'api_key': api_key}

    r = requests.get(url, params=payload)
    r.raise_for_status()

    json = r.json()
    images_json = json['images']
    base_url = images_json['base_url']
    available_sizes = images_json['poster_sizes']
    poster_size = None

    for size in example_sizes:
        if size in available_sizes:
            poster_size = size
            break

    return base_url + poster_size


# Loading API /configuration
image_base_url = get_image_base_url(API_KEY)

log.info('Opening movies files...')
with open('csv/pre-movies.csv', newline='') as original_file, open('csv/movies.csv', 'w', newline='') as final_file:
    reader = csv.reader(original_file, delimiter=',')
    next(reader, None)  # skip the headers

    writer = csv.writer(final_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['_id', 'title', 'genres', 'poster'])  # prepare headers

    for row in reader:
        localID = row[0]
        title = row[1]
        genres = row[2]

        log.info('Local ID: {}'.format(localID))
        poster = get_poster_for_title(title)

        if poster:
            poster = image_base_url + poster
        else:
            log.warn('No poster for ID: {} Title: "{}"'.format(localID, title))
            poster = ''

        writer.writerow([localID, title, genres, poster])
