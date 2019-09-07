#!/usr/bin/env python3

import logging
import itertools
import geopandas as gpd
import pandas as pd

from . import Analysis
from .. import defaults
from shapely.wkt import loads as wktToLineString

class SimpleAnalysis(Analysis):
    '''
    Example of an Analysis class that can be written on top of a ScenarioAPI.

    Parameters
    ----------
    api: ScenarioAPI
        ScenarioAPI to be queried for the SimpleAnalysis
    '''

    def __init__(self, api):
        self.log = logging.getLogger(defaults.LOGGER)
        self.api = api

    def time_matrix(self, origins, dests, origin_id_col=None, dest_id_col=None):
        '''
        Return a time matrix of origins to destinations, in a DataFrame.

        Parameters
        ----------
        origins: POIDataset
            Origin points to be used in time matrix (these will be returned as rows)
        dests: POIDataset
            Destination points to be used in time matrix (these will be returned as columns)
        origin_id_col: str, optional
            Column in origins dataset to be used as index for time matrix. ID col must be unique if specified; if not, the row index will be used
        dest_id_col: str, optional
            Column in dests dataset to be used as index for time matrix. ID col must be unique if specified; if not, the row index will be used

        Returns
        -------
        pd.GeoDataFrame
            Matrix dataframe of time, in seconds, from each origin to each destination.
        '''

        self.log = logging.getLogger("tebetebe")

        ## From
        origin_ids = list(origins[origin_id_col]) if origins_id_col else origins.index.tolist()
        origin_coords = self._get_coords_list(origins)

        dest_ids = list(dests[dest_id_col]) if dest_id_col else dests.index.tolist()
        dest_coords = self._get_coords_list(dests)

        try:
            (matrix, from_snap, to_snap) = self.api.table(origin_coords,
                                                          coords_dest = dest_coords,
                                                          ids_origin = origin_ids,
                                                          ids_dest = dest_ids,
                                                          output = "pandas")

            return matrix

        except Exception as exc:
            self.log.error(exc)

    def get_routes(self, origins, dests, origin_id_col=None, dest_id_col=None):
        '''
        Get a GeoDataFrame of routes between each origin and destination. This is
        probably not the most efficient way to do this! Both datasets should be in EPSG:4326

        Parameters
        ----------
        origins: POIDataset
            Origin points to be used in routing
        dests: POIDataset
            Destination points to be used in routing
        origin_id_col: str, optional
            Column in origins dataset to be used as origin_id row in returned GDF. ID col must be unique if specified; if not, the row index will be used
        dest_id_col: str, optional
            Column in dests dataset to be used as dest_id row in returned GDF. ID col must be unique if specified; if not, the row index will be used

        Returns
        -------
        gpd.GeoDataFrame
            Data Frame with "origin_id", "dest_id", "time", "dist" columns, and a geometry column with the route calculated by OSRM.
        '''

        ## Use index if id_cols not spefcified
        if not origin_id_col:
            origin_id_col = "id"
            origins["id"] = origins.index.tolist()
        if not dest_id_col:
            dest_id_col = "id"
            dests["id"] = dests.index.tolist()

        ## Get DF of all pairwise origin and dest ids
        permutations = itertools.product(*[origins[origin_id_col], dests[dest_id_col]])
        origins_dests = pd.DataFrame(list(permutations), columns=["origin_id", "dest_id"])

        ## Trim down to and from DFs into just the id and geometry, then merge to routes_df
        origins_df = origins[[origin_id_col,"geometry"]].rename(columns={origin_id_col: "origin_id", "geometry": "origin_geom"})
        dests_df = dests[[dest_id_col,"geometry"]].rename(columns={dest_id_col: "dest_id", "geometry": "dest_geom"})

        routes_df = origins_dests.merge(origins_df).merge(dests_df)

        ## Add on distance and geometry columns
        ## -1 so if something goes wrong, we can tell it's bad in the output
        routes_df["dist"] = -1
        routes_df["time"] = -1
        routes_df["geometry"] = None

        ## Not the most efficient, I'm sure
        for idx, to_from in routes_df.iterrows():
            origin_coords = (to_from.origin_geom.x, to_from.origin_geom.y)
            dest_coords = (to_from.dest_geom.x, to_from.dest_geom.y)

            try:
                route = self.api.simple_route(origin_coords,
                                              dest_coords,
                                              geometry="wkt",
                                              overview="full")

                routes_df.at[idx, "time"] = route["routes"][0]["duration"]
                routes_df.at[idx, "dist"] = route["routes"][0]["distance"]
                routes_df.at[idx, "geometry"] = wktToLineString(route["routes"][0]["geometry"])

            except Exception as exc:
                self.log.error(exc)


        routes_df.drop(["origin_geom", "dest_geom"], axis=1, inplace=True)

        return gpd.GeoDataFrame(routes_df)

    def _get_coords_list(self, gdf):
        return gdf.geometry.apply(lambda c: [c.centroid.x, c.centroid.y]).tolist()

