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
    Extension of a GeoDataFrame which stores Points only, to be used as origin, destination,
    and waypoints in routing.

    Parameters
    ----------
    name: str
        Name of POIDataset (required)
    '''
    def __init__(self, *args, name=None, **kwargs):

        if name is None:
            raise ValueError("Must specify name for POIDataset")
        else:
            setattr(self, "_metadata", {"name": name})

        super(POIDataset, self).__init__(*args, **kwargs)

    def get_name(self):
        """Return POI dataset name"""
        return self._metadata["name"]

    def _filter_points(self, gdf):
        '''Filter out any records in GeoDataFrame that are not Point geometries'''

        gdf_geom_types = gdf.apply(lambda r: r.geometry.type, axis=1)
        gdf_points = gdf[gdf_geom_types == "Point"]

        return gdf_points

    @classmethod
    def from_overpass(cls, query, name=None, overwrite=False, tmp_dir=defaults.TMP_DIR, **kwargs):
        '''
        Initialize POIDataset from Overpass API query. Any returned nodes or closed ways with `center` attributes will be included in the dataset.

        Parameters
        ----------
        query : str
            Query to be sent to overpass API. This query should *not* include an `out` directive (eg. [out:json];)
        name : str
            Name of the POI dataset
        overwrite : bool
            Overwrite POIDataset if it already exists on disk
        tmp_dir : str
            Temporary directory to save POIDataset
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
                return cls.from_file(out_file, name=out_name).set_index("id")


        logger.info("Downloading POIDataset {}".format(name))

        ## Query API
        oapi = overpass.API()
        json = oapi.get("[out:json];{}".format(query),
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

        return cls.from_features(pois.features, name=out_name, crs={'init': 'epsg:4326'}) \
                  .set_index("id")

    @classmethod
    def from_file(cls, path, name=None, **kwargs):
        '''Initialize POIDataset from file. If no name is given, the filename will be used'''

        gdf = GeoDataFrame.from_file(path, **kwargs)
        gdf_points = cls._filter_points(cls, gdf)

        return cls(gdf_points, name=name if name else Path(path).stem)

    @classmethod
    def from_features(cls, features, name=None, **kwargs):
        '''Initialize POIDataset from GeoJSON features'''

        gdf = GeoDataFrame.from_features(features, **kwargs)
        gdf_points = cls._filter_points(cls, gdf)

        return cls(gdf_points, name=name)
