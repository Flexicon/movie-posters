#!/usr/bin/python3
import requests
import csv
import logging
from imdb import IMDb


def getPosterForTitle(title):
    log.info('Search for movies by title: {}...'.format(title))
    res = IA.search_movie(title)
    poster = None

    if res and len(res):
        log.info('Found {} movies'.format(len(res)))
        for movie in res:
            log.info('Looking up by id: {}...'.format(movie.movieID))

            fullMovie = IA.get_movie(movie.movieID)
            poster = fullMovie.get('cover')

            log.info('Movie found, cover: {}'.format(poster))
            if poster:
                break

    return poster


def savePoster(poster, filename):
    with open('images/' + filename + '.jpg', 'wb') as handle:
        response = requests.get(poster, stream=True)

        if not response.ok:
            log.error('Failed downloading cover image: {}'.format(response))
        else:
            for block in response.iter_content(1024):
                if not block:
                    break
                handle.write(block)


# Setup logger
logging.basicConfig(
    format='%(levelname)s: %(asctime)s %(message)s',
    datefmt='%H:%M:%S'
)
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# Setup IMDb API lib
IA = IMDb()

log.info('Opening movies file...')
with open('csv/movies.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader, None)  # skip the headers
    for row in reader:
        localID = row[0]
        title = row[1]

        log.info('Local ID: {}'.format(localID))
        poster = getPosterForTitle(title)
        if poster:
            savePoster(poster, localID)
        else:
            log.warn('No poster for ID: {} Title: "{}"'.format(localID, title))
