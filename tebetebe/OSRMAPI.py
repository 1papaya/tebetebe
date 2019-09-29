from polyline.codec import PolylineCodec
from shapely.geometry import Point
from . import Scenario
from . import defaults

import geopandas as gpd
import osrm_api
import logging
import json

## shapely: x = longitude; y = latitude
## osrm:    (lon, lat)

class OSRMAPI():
    def __init__(self, url, version="v1", profile="skobuffs"):
        self.log = logging.getLogger(defaults.LOGGER)

        ## Scenario API path settings
        self.url = url
        self.api_config = osrm_api.Configuration(host=self.url)
        self.api_client = osrm_api.ApiClient(configuration=self.api_config)
        self.api = osrm_api.OSRMApi(self.api_client)

        ## API Path Requests defaults. Currently not recognized by OSRM API
        self.profile = profile
        self.version = version

    def nearest(self, coord, response="raw", **kwargs):
        coord = self._coord_to_tuple(coord)
        kwargs = self._serialize_params(kwargs)

        ## Send API Request
        try:
            api_resp = self.api.nearest(self.version, self.profile,
                                        "{},{}".format(coord[0], coord[1]), **kwargs)

            ## Honor response type
            if response == "raw":
                return api_resp

            elif response in ["dict", "gdf"]:
                w_list = []

                for w in api_resp['waypoints']:
                    w_list.append(self._waypoint_to_dict(w))

                if response == "dict":
                    return w_list
                elif response == "gdf":
                    return gpd.GeoDataFrame(w_list)

        except osrm_api.ApiException as exc:
            ## Issue warning for OSRM HTTP API Error.
            ## This can be further debugged by passing routed_args={"verbose":True} to Scenario
            if exc.status == 400:
                resp = json.loads(exc.body)

                self.log.warning("HTTP 400: {}: {}".format(resp["code"], resp["message"]))
                return None

    def route(self, coords, response="raw", **kwargs):
        coords = [self._coord_to_tuple(coord) for coord in coords]
        kwargs = self._serialize_params(kwargs)

        ## Send req as polyline
        try:
            api_resp = self.api.route(self.version, self.profile,
                                      ";".join(["{},{}".format(c[0], c[1]) for c in coords]), ## serialize
                                      **kwargs)

            if response == "raw":
                return api_resp

        except osrm_api.ApiException as exc:
            ## Issue warning for OSRM HTTP API Error.
            ## This can be further debugged by passing routed_args={"verbose":True} to Scenario
            if exc.status == 400:
                resp = json.loads(exc.body)

                self.log.warning("HTTP 400: {}: {}".format(resp["code"], resp["message"]))
                return None

    def _serialize_params(self, params):
        """Serialize params with semicolons if necessary"""
        semicolon_delimited = ["bearings", "radiuses", "hints", "sources", "destinations", "timestamps"]

        for key, value in params.items():
            if key in semicolon_delimited:
                params[key] = ";".join(value)

        return params

    def _coord_to_tuple(self, coord):
        '''Convert a coordinate of varying data types to a tuple'''
        if isinstance(coord, tuple):
            return coord
        elif isinstance(coord, Point):
            return (coord.x, coord.y)
        elif isinstance(coord, list):
            return (coord[0], coord[1])
        elif isinstance(coord, dict):
            return (coord["x"], coord["y"])

    def _waypoint_to_dict(self, w):
        '''Convert a 'waypoint' OSRM response to dictionary with geometry'''
        w_dict = {
            "name": w['name'],
            "distance": w['distance'],
            "hint": w['hint'],
            "geometry": Point(w['location'][0], w['location'][1])
        }

        if "nodes" in w:
            w_dict["from_node_id"] = w["nodes"][0]
            w_dict["to_node_id"] = w["nodes"][1]

        return w_dict