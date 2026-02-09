"""
Movie package - contains all movie-related classes and functions.
"""

# Import main classes to make them available at package level
from .rating import MovieRating, get_rating
from .movie import (
    Movie,
    ActionAdventure,
    Comedy,
    Drama,
    Horror,
    Romance,
    ScienceFictionFantasy,
    Western,
    create_movie
)

# Define what gets imported with "from module02.movie import *"
__all__ = [
    'MovieRating',
    'get_rating',
    'Movie',
    'ActionAdventure',
    'Comedy',
    'Drama',
    'Horror',
    'Romance',
    'ScienceFictionFantasy',
    'Western',
    'create_movie'
]

# Package metadata
__version__ = '1.0.0'
__author__ = 'Christophe Van Heck'