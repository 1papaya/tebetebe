#!/usr/bin/env python3

import overpass
import hashlib
import logging

from pathlib import Path

from .utils import hash_
from . import defaults

class RouteNetwork():
    '''
    .osm file from which a route network will be extracted

    Parameters
    ----------
    path:
        Path to *.osm{.pbf} dataset
    name: str
        Name of OSMDataset
    '''

    def __init__(self, path, name=None, **kwargs):

        self.log = logging.getLogger(defaults.LOGGER)
        self.path = Path(path)

        ## Check path exists
        if not self.path.is_file():
            raise FileNotFoundError("OSM Dataset Not Found ({})".format(path))

        ## Set profile name to filename if not specified
        self.name = name if name else self.path.stem.split(".")[0]

    def get_name(self):
        """Return route network name"""
        return self.name

    def get_path(self):
        """Return route network path"""
        return self.path

    @classmethod
    def from_overpass(cls, query, name=None, overwrite=False, tmp_dir=defaults.TMP_DIR, **kwargs):
        '''
        Initialize a RouteNetwork by downloading result of an overpass query and saving as .osm

        Parameters
        ----------
        query : str
            Query to be sent to overpass API. This query *must* output in XML! (eg. [out:xml];)
        name : str
            Name of the route network
        overwrite : bool
            Overwrite route network if it already exists on disk
        tmp_dir : str
            Temporary directory to save route network

        Returns
        -------
        OSMDataset
        '''

        logger = logging.getLogger(defaults.LOGGER)

        ## Use md5 hash of query as filename if name not specified
        out_folder = Path(tmp_dir)
        out_name = name if name else hash_(query)
        out_file = out_folder / "{}.osm".format(out_name)

        ## Honor overwrite settings
        if out_file.is_file():
            if overwrite:
                logger.info("Overwriting {}".format(out_file))
                out_file.unlink()
            else:
                logger.info("Using existing OSMDataset {}".format(out_file))
                return cls(out_file, name=name, overwrite=overwrite, tmp_dir=tmp_dir)

        ## Query API
        oapi = overpass.API()
        xml = oapi.get(query,
                       verbosity="geom",
                       responseformat="xml",
                       build=False)

        ## Save file
        out_folder.mkdir(parents=True, exist_ok=True)
        out_file.write_text(xml)

        return cls(out_file, name=name, overwrite=overwrite, tmp_dir=tmp_dir)
