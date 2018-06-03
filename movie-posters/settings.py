import os
import logging

# Setup logger
logging.basicConfig(
    format='%(levelname)s: %(asctime)s %(message)s',
    datefmt='%H:%M:%S'
)
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# Setup API lib
from tmdbv3api import TMDb, Movie

# Constant to hold key
API_KEY = os.getenv('TMDB_API_KEY')

tmdb = TMDb()
tmdb.api_key = API_KEY
MOVIE_API = Movie()
