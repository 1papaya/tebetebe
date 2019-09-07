#!/usr/bin/env python3

import geojson as gj
import overpass
import logging

from geopandas import GeoDataFrame
from pathlib import Path

from .utils import hash_
from . import defaults

class POIDataset(GeoDataFrame):
    '''
    Extension of a GeoDataFrame which stores only points, and which provides
    a method to load from the Overpass API

    Parameters
    ----------
    name: str
        Name of POIDataset
    '''
    def __init__(self, *args, name=None, **kwargs):

        ## Set POIDataset name
        if name is None:
            raise ValueError("Must specify name for POIDataset")
        else:
            self.set_name(name)

        super(GeoDataFrame, self).__init__(*args, **kwargs)

        ## TODO figure out why this is sometimes necessary...
        if not hasattr(self, "crs"):
            self.crs = {'init': 'epsg:4326'}

    def set_name(self, name):
        '''
        Set name of POIDataset

        Parameters
        ----------
        name : str
            Name to set as POIDataset name
        '''

        if hasattr(self, "_metadata") and isinstance(self._metadata, dict):
            self._metadata["name"] = name
        else:
            self._metadata = {"name": name}

    def get_name(self): return self._metadata["name"]

    def _filter_points(self, gdf):
        '''
        Filter out any records in GeoDataFrame that are not Point geometries

        Parameters
        ----------
        gdf : geopandas.GeoDataFrame
            GeoDataFrame to be filtered

        Returns
        -------
        geopandas.GeoDataFrame
            Filtered GeoDataFrame
        '''

        gdf_geom_types = gdf.apply(lambda r: r.geometry.type, axis=1)
        gdf_points = gdf[gdf_geom_types == "Point"]

        return gdf_points

    @classmethod
    def from_overpass(cls, query, name=None, overwrite=False, tmp_dir=defaults.TMP_DIR, **kwargs):
        '''
        Download overpass query, parse for nodes returned and return initialize POIDataset

        Parameters
        ----------
        query : str
            Query to be sent to overpass API. This query *must* output in JSON! (eg. [out:json];)
        name : str
            Name of the POI dataset
        overwrite : bool
            Overwrite POIDataset if it already exists on disk
        tmp_dir : str
            Temporary directory to save POIDataset

        Returns
        -------
        POIDataset
        '''
        
        logger = logging.getLogger(defaults.LOGGER)

        ## Use md5 hash of query as filename if name not specified
        out_folder = Path(tmp_dir)
        out_name = name if name else hash_(query)
        out_file = out_folder / "{}.geojson".format(out_name)

        ## Honor overwrite settings
        if out_file.is_file():
            if overwrite:
                logger.info("Overwriting {}".format(out_file))
                out_file.unlink()
            else:
                logger.info("Using existing POIDataset {}".format(out_file))
                return cls.from_file(out_file, name=out_name)

        ## Query API
        oapi = overpass.API()
        json = oapi.get(query,
                        verbosity="geom",
                        responseformat="json",
                        build=False)

        ## Filter response and convert to FeatureCollection
        features = []

        for el in json['elements']:
            ## Only look at ways & nodes
            if not "type" in el or el['type'] not in ["way", "node"]:
                continue

            ## Discard ways without center points
            if el['type'] == "way" and "center" in el:
                feat = gj.Feature(geometry = gj.Point((el['center']['lon'], el['center']['lat'])),
                                  properties = {**{"id": el['id']}, **el['tags']})

            elif el['type'] == "node":
                feat = gj.Feature(geometry = gj.Point((el['lon'], el['lat'])),
                                  properties = {**{"id": el['id']}, **el['tags']})

            else:
                continue

            features.append(feat)

        pois = gj.FeatureCollection(features)

        ## Cache POIs for next time
        out_folder.mkdir(parents=True, exist_ok=True)
        out_file.write_text(gj.dumps(pois))

        return cls.from_features(pois.features, name=out_name, crs={'init': 'epsg:4326'})

    @classmethod
    def from_file(cls, path, *args, name=None, **kwargs):
        '''
        Load POIDataset from file

        Parameters
        ----------
        path : str
            Path of file to be loaded. Can be any OGR dataset that is readable by fiona/geopandas
        name : str
            Name of dataset

        Returns
        -------
        POIDataset
        '''

        gdf = super(POIDataset, cls).from_file(path, *args, **kwargs)
        gdf_points = cls._filter_points(cls, gdf)

        return cls(gdf_points, name=name)

    @classmethod
    def from_features(cls, features, *args, name=None, **kwargs):
        '''
        Load POIDataset from GeoJSON features

        Parameters
        ----------
        features : array of geojson.Feature
            Features to convert into GeoDataFrame
        name : str
            Name of dataset

        Returns
        -------
        POIDataset
        '''

        gdf = super(POIDataset, cls).from_features(features, *args, **kwargs)
        gdf_points = cls._filter_points(cls, gdf)

        return cls(gdf_points, name=name)