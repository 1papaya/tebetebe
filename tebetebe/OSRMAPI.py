from shapely.geometry import Point
from . import Scenario
from . import defaults

import geopandas as gpd
import osrm_api
import polyline
import logging
import json

## TODO more response=* for nearest, route, ...

class OSRMAPI():
    def __init__(self, host, version="v1", profile="skobuffs"):
        self.log = logging.getLogger(defaults.LOGGER)

        ## Initialize osrm-openapi as "sub-api"
        self.host = host
        self.api = self._get_api_for_host(self.host)

        ## API Path Requests constants. Currently different versions/profiles are not supported
        self.profile = profile
        self.version = version

    def nearest(self, coord, number=1, response="raw", **kwargs):
        coord = self._coord_to_tuple(coord)
        kwargs = self._serialize_params(kwargs)

        ## Send API Request
        try:
            api_resp = self.api.nearest(self.version, self.profile,
                                        "{},{}".format(coord[0], coord[1]), number, **kwargs)

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
            self._handle_osrm_error(exc)
            return None

    def route(self, coords, response="raw", **kwargs):
        coords = [self._coord_to_tuple(coord) for coord in coords]
        kwargs = self._serialize_params(kwargs)

        try:
            api_resp = self.api.route(self.version, self.profile,
                                      self._polyline(coords), **kwargs)

            if response == "raw":
                return api_resp

        except osrm_api.ApiException as exc:
            self._handle_osrm_error(exc)
            return None

    def is_alive(self):
        """Send a lil' request to OSRM server to see if it responds"""
        try:
            resp = self.nearest((0,0))
            return True
        except Exception as exc:
            return False

    def _get_api_for_host(self, host):
        """Return osrm-openapi API for a host"""
        api = osrm_api.OSRMApi()
        api.api_client.configuration.host = host

        return api

    def _polyline(self, coords):
        """Turn coordinates into polyline in format OSRM accepts"""
        ## geojson=True to use pairs as lat, lon tuples
        return "polyline({})".format(polyline.encode(coords, geojson=True))

    def _handle_osrm_error(self, exc):
        ## Issue warning for OSRM HTTP API Error.
        ## This can be further debugged by passing routed_args={"verbose":True} to Scenario
        if exc.status == 400:
            resp = json.loads(exc.body)
            self.log.warning("HTTP 400: {}: {}".format(resp["code"], resp["message"]))

    def _serialize_params(self, params):
        """Serialize params with semicolons if necessary"""
        semicolon_delimited = ["bearings", "radiuses", "hints", "sources", "destinations", "timestamps"]

        for key, value in params.items():
            ## Semicolon delimited parameters
            if key in semicolon_delimited:
                params[key] = ";".join(value)
            ## Make boolean parameters lowercase
            elif isinstance(value, bool):
                params[key] = str(value).lower()

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
