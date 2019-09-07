#!/usr/bin/env python3

import logging

from pathlib import Path
from . import defaults

class RoutingProfile():
    '''
    RoutingProfile is a .lua file with directives on how to turn a RouteNetwork
    into a routable OSRM file

    Parameters
    ----------
    path: str
        Path to .lua file. Note that all files referenced within that file (WayHandlers, etc) are relative to the .lua file path.
    name: str, optional
        Name of routing profile
    '''

    def __init__(self, path, name=None, **kwargs):
        self.log = logging.getLogger(defaults.LOGGER)
        self.path = Path(path)

        ## Check path exists
        if not self.path.is_file():
            raise FileNotFoundError("Routing Profile Not Found ({})".format(path))

        ## Set profile name to lua filename if not specified
        self.name = name if name else self.path.stem

    def get_name(self): return self.name
    def get_path(self): return self.path
