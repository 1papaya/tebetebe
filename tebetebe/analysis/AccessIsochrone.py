from osrm import AccessIsochrone as OSRMAccessIsochrone
from shapely.geometry import MultiPolygon

class AccessIsochrone(OSRMAccessIsochrone):
    """
    Compute an access isochrone from an origin point with a given `ScenarioAPI`

    Parameters
    ----------
    scenario : Scenario
        Scenario to be queried for access isochrone
    point_origin : 2-floats tuple
        The coordinates of the center point to use as (x, y).
    points_grid : int
        The number of points of the underlying grid to use.
    size : float
        Search radius (in wgs84 degrees)
    """
    def __init__(self, scenario, point_origin, points_grid=500, size=0.4):

        super(AccessIsochrone, self).__init__(point_origin, points_grid, size,
                                              url_config = scenario.config)

    def get_center(self):
        """Return center point used in isochrone calculations"""
        return self.center_point

    def get_grid(self):
        """Return GeoDataFrame of grid used in duration calculations, snapped to the road network"""
        return self.grid

    def get_durations(self):
        """Return durations table retrieved from OSRM"""
        return self.times

    def render_contour(self, n_levels):
        """Return GeoDataFrame of MultiPolygon contours for a specified number of levels """

        contours = super(AccessIsochrone, self).render_contour(n_levels)

        ## osrm.AccessIsochrone.render_contour returns a GeoDataFrame with mixed
        ## Polygon/Multipolygon geometries. This ensures all geometries are multipolygons
        ## and renames the `time` field which is a special column for many data types and
        ## causes issues on export
        contours.geometry = contours.geometry.apply(lambda g: MultiPolygon([g]) if g.type == "Polygon" else g)
        contours.rename(columns={"time": "duration"}, inplace=True)

        return contours
