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
    lua_path: str
        Path to .lua file. Note that all files referenced within that file (WayHandlers, etc) are relative to the .lua file path.
    name: str, optional
        Name of routing profile. If not provided, the .lua filename is used.
    '''

    def __init__(self, lua_path, name=None, **kwargs):
        self.log = logging.getLogger(defaults.LOGGER)
        self.path = Path(lua_path)

        ## Check path exists
        if not self.path.is_file():
            raise FileNotFoundError("Routing Profile Not Found ({})".format(lua_path))

        ## Set profile name to lua filename if not specified
        self.name = name if name else self.path.stem

    def get_name(self):
        """Return name of routing profile"""
        return self.name

    def get_path(self):
        """Return path of routing profile"""
        return self.path
