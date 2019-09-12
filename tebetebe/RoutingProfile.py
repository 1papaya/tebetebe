#!/usr/bin/env python3

import logging

from pathlib import Path
from . import defaults

class RoutingProfile():
    '''
    A RoutingProfile is a configuration script which represents a routing behaviour, such
    as for bike or car routing. It describes whether or not to traverse a particular type
    of way or node in OSM data, and the speed at which those elements are traversed.

    Check out the osrm-backend wiki for more information!
    https://github.com/Project-OSRM/osrm-backend/wiki/Profiles

    Parameters
    ----------
    lua_path: str
        Path to .lua configuration script
    name: str, optional
        Name of routing profile. If not provided, the .lua filename is used.
    default: bool, optional
        If RoutingProfile is a default profile
    '''

    def __init__(self, lua_path, name=None, default=False, **kwargs):
        self.log = logging.getLogger(defaults.LOGGER)
        self.path = Path(lua_path)
        self.default = default

        ## Check path exists
        if not self.path.is_file():
            raise FileNotFoundError("Routing Profile Not Found ({})".format(lua_path))

        ## Set profile name to lua filename if not specified
        self.name = name if name else self.path.stem

    def is_default(self):
        """Return if routing profile is a default or not"""
        return self.default

    def get_name(self):
        """Return name of routing profile"""
        return self.name

    def get_path(self):
        """Return path of routing profile"""
        return self.path
