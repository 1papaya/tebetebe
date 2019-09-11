#!/usr/bin/env python3

from .RoutingProfile import RoutingProfile
from .Environment import Environment
from .OSMDataset import OSMDataset
from .POIDataset import POIDataset
from .Scenario import Scenario

from . import defaults

##
## Logger configuration
##

from logging.config import dictConfig

dictConfig({
    "version": 1,
    'formatters': {
        'f': {
            'format': '[%(levelname)7s] %(message)s',
            'datefmt': '%H:%M:%S'
        }
    },
    'handlers': {
        'h': {
            'class': 'logging.StreamHandler',
            'formatter': 'f',
            'level': 0
        }
    },
    'loggers': {
        defaults.LOGGER: {
        'handlers': ['h'],
        'level': defaults.LOGGER_LEVEL
        }
    },
})
