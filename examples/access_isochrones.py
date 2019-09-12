from tebetebe.analysis import AccessIsochrone
from tebetebe.profiles import car
import tebetebe as tb

tb_env = tb.Environment(tmp_dir="./tmp/access_isochrones")
mbabane = (31.1367, -26.3054)

## Initialize scenario with GeoFabrik extract and default car profile
scenario = tb_env.Scenario("./tmp/swaziland-latest.osm.pbf", car)

## Compile and run scenario
with scenario() as api:
    isochrone = AccessIsochrone(api, mbabane, points_grid=1000, size=0.2)
    contours = isochrone.render_contour(10)

    ## Save contours as GeoJSON for visualization with QGIS
    contours.to_file(tb_env.tmp_dir / "contour10.geojson", driver="GeoJSON")
