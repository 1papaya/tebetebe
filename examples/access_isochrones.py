from tebetebe.analysis import AccessIsochrone
import tebetebe as tb

tb_env = tb.Environment(tmp_dir="./tmp/access_isochrones",
                        overwrite=False, verbose=False)

mbabane = (31.1367, -26.3054)

## Initialize scenario with extract from GeoFabrik and car profile
## http://download.geofabrik.de/africa/swaziland-latest.osm.pbf
scenario = tb_env.Scenario("./tmp/access_isochrones/swaziland-latest.osm.pbf",
                           "./profiles/car.lua")

## Run scenario
with scenario() as api:
    isochrone = AccessIsochrone(api, mbabane, points_grid=1000, size=0.2)
    contours = isochrone.render_contour(10)

    ## Save contours as GeoJSON for visualization with QGIS
    contours.to_file(tb_env.tmp_dir / "contour10.geojson", driver="GeoJSON")
