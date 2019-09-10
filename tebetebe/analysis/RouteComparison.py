from .. import defaults

from shapely.wkt import loads as wktToLineString

import geopandas as gpd
import pandas as pd
import numpy as np
import itertools
import logging

class RouteComparison():
    """
    Compare route differences between scenarios

    Parameters
    ----------
    origins: POIDataset
        Points to be used as the origins in route comparison
    dests: POIDataset
        Points to be used as the destinations in route comparison
    origins_id_col: str, optional
        Column in `origins` dataset to be used as ID. Must be unique. If not specified, the index will be used
    dests_id_col: str, optional
        Column in `dests` dataset to be used as ID. Must be unique. If not specified, the index will be used
    cache: bool, optional
        Whether to cache time matrices
    """

    def __init__(self, origins, dests, origins_id_col=None, dests_id_col=None, cache=True):

        ## Set POIDataset indexes to id cols if specified, otherwise use row index
        self.origins = origins.set_index(origins_id_col) if origins_id_col else origins
        self.dests = dests.set_index(dests_id_col) if dests_id_col else dests

        ## Get a DataFrame of all origin_id:dest_id pairs; od=origin:dest
        self.od_pairs = self._get_index_pairs(self.origins, self.dests) \
                            .rename(columns={0: "origin_id", 1: "dest_id"})

        ## Set up cache
        self.cache = cache
        self.duration_matrix = {}

    ##
    ## Base Functions

    def get_duration_matrix(self, scenario, melted=False):
        """
        Calculate a duration matrix between `origins` and `dests`

        Parameters
        ----------
        scenario: Scenario
            Scenario to run calculate the duration matrix on
        melted: bool, optional
            Whether the matrix should be returned as a matrix DF, or melted into `origin_id` `dest_id` and `duration` columns

        Returns
        -------
        pd.DataFrame
            Duration Matrix DataFrame
        """

        s = scenario.get_name()

        ## If hasn't been computed or cache is off
        if s not in self.duration_matrix:

            origin_ids = self.origins.index.tolist()
            origin_coords = self.origins.geometry.apply(lambda o: (o.x, o.y)).tolist()

            dest_ids = self.dests.index.tolist()
            dest_coords = self.dests.geometry.apply(lambda d: (d.x, d.y)).tolist()

            (matrix, origin_snap, dest_snap) \
                = scenario.table(origin_coords,
                                 coords_dest = dest_coords,
                                 output = "np")

            ## Transform matrix to proper dataframe with index&columns
            matrix = pd.DataFrame(matrix, columns = dest_ids, index = origin_ids)

            if self.cache:
                self.duration_matrix[s] = matrix
            else:
                return matrix

        return self.duration_matrix[s] if not melted else self._melt_duration_matrix(self.duration_matrix[s], scenario)

    def get_routes(self, scenario, od_pairs=None):
        """
        Get routes between origins and dests

        Parameters
        ----------
        scenario: Scenario
            Scenario on which the origin:dest routes will be calculated
        od_pairs: pd.DataFrame, optional
            DataFrame of origin:dest pairs in two columns `origin_id` and `dest_id` for calculation. If not specified, all pairwise origin:dest routes will be calculated.

        Returns
        -------
        GeoDataFrame
           GDF with duration, distance, and route geometry for each origin:dest pair
        """

        s = scenario.get_name()

        origins_geom = self.origins.geometry.apply(lambda o: (o.x, o.y)).rename("origin_geom")
        dests_geom = self.dests.geometry.apply(lambda d: (d.x, d.y)).rename("dest_geom")

        ## If origins_dests pairs are not given, use all 
        if od_pairs is None:
            od_pairs = self.od_pairs

        ## Assemble dataframe with `origin_id`, `dest_id`, `origin_geom`, `dest_geom`
        routes = od_pairs.merge(origins_geom.to_frame(), left_on="origin_id",
                                right_index=True) \
                         .merge(dests_geom.to_frame(), left_on="dest_id",
                                right_index=True)

        ## Calculate an OSRM simple_route for a given diff_routes row
        def route_from_row(api, row):
            route = api.simple_route(row["origin_geom"], row["dest_geom"],
                                     geometry = 'wkt', overview="full")

            r_index = ["{}_duration".format(s), "{}_distance".format(s), "geometry"]

            return pd.Series([route['routes'][0]['duration'],
                              route['routes'][0]['distance'],
                              wktToLineString(route["routes"][0]["geometry"])],
                             index=r_index)

        route_info = routes.apply(lambda r: route_from_row(scenario, r),
                                  result_type="expand", axis=1)

        ## Drop point geoms and scenario duration from routes DF (if exists. it will be added
        ## by route_info anyway). Then, join to route info returned, then return GDF
        routes.drop(columns=['origin_geom', 'dest_geom', '{}_duration'.format(scenario.get_name())],
                    inplace=True, errors="ignore")

        return gpd.GeoDataFrame(routes.join(route_info))

    def get_duration_table(self, *args):
        """
        Get route duration table for multiple scenarios

        Parameters
        ----------
        *args
            Arbitrary number of scenarios to run duration table

        Returns
        -------
        DataFrame
            DF of origin:dest pairs and durations for each scenario
        """

        table = self.get_duration_matrix(args[0], melted=True)

        for s_idx in range(1, len(args)):
            table = table.merge(self.get_duration_matrix(args[s_idx], melted=True))

        return table

    ##
    ## Higher level

    def get_difference(self, scenario0, scenario1):
        """Get DF of origin:dest pairs whos routes differ between scenarios"""
        duration_table = self.get_duration_table(scenario0, scenario1)

        s0_duration = duration_table['{}_duration'.format(scenario0.get_name())]
        s1_duration = duration_table['{}_duration'.format(scenario1.get_name())]

        return duration_table[s0_duration != s1_duration]

    def get_same(self, scenario0, scenario1):
        """Get DF of origin:dest pairs whos routes are the same between scenarios"""
        duration_table = self.get_duration_table(scenario0, scenario1)

        s0_duration = duration_table['{}_duration'.format(scenario0.get_name())]
        s1_duration = duration_table['{}_duration'.format(scenario1.get_name())]

        return duration_table[s0_duration == s1_duration]

    ##
    ## Utils

    def _get_index_pairs(self, df0, df1):
        df0_ids = df0.index.tolist()
        df1_ids = df1.index.tolist()

        return pd.DataFrame(list(itertools.product(df0_ids, df1_ids)))

    def _melt_duration_matrix(self, matrix, scenario):
        """Melt a duration matrix into an origin_id:dest_id DF with duration"""

        index_rename = {"level_0": "origin_id",
                        "level_1": "dest_id"}

        return matrix.stack().reset_index() \
                             .rename(columns={
                                 **index_rename,
                                 **{0: "{}_duration".format(scenario.get_name())}
                             })
