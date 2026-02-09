"""
Person package - contains Person class and related functions.
"""

# Import main classes to make them available at package level
from .person import Person, get_person

# Define what gets imported with "from module02.person import *"
__all__ = [
    'Person',
    'get_person'
]

# Package metadata
__version__ = '1.0.0'
__author__ = 'Christophe Van Heck'