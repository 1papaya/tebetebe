from tebetebe.analysis import ParallelScenarios, RouteComparison
import tebetebe as tb

tb_env = tb.Environment(tmp_dir="./tmp/scenario_comparison")

## Get route network from GeoFabrik extract and POIs from Overpass API
## Load the route origins (homesteads) and dests (schools) 8km around river crossing
crossing_node_id = 6750683291
highways = tb_env.OSMDataset("./tmp/swaziland-latest.osm.pbf", name="swazi")
homesteads = tb_env.POIDataset.from_overpass("""node({})->.crossing;
                                                 ( way(around.crossing:8000)["building"];);
                                                out center;""".format(crossing_node_id),
                                             name="homesteads")
schools = tb_env.POIDataset.from_overpass("""node({})->.crossing;
                                                 ( way(around.crossing:8000)["amenity"="school"];);
                                                out center;""".format(crossing_node_id),
                                          name="schools")

## Normal & Flood scenarios. Pass along an extra parameter to osrm-routed
## so that the max duration table size is enough for all origin:dest pairs
routed_args = {"max_table_size": len(homesteads) * len(schools) + 1}

normal = tb_env.Scenario(highways, "./profiles/walk_normal.lua",
                         routed_args=routed_args, name="normal")
flood = tb_env.Scenario(highways, "./profiles/walk_flood.lua",
                        routed_args=routed_args, name="flood")

## Run normal and flood scenarios in parallel
parallel_scenarios = ParallelScenarios(normal, flood)

with parallel_scenarios as scenarios:
    ## Compare origin:dest routes
    comparison = RouteComparison(origins=homesteads, dests=schools)

    ## Routes that are different between scenarios
    flood_affected = comparison.get_difference(normal, flood)

    ## Point dataframe of all homesteads who are flood affected
    homesteads[homesteads.index.isin(flood_affected['origin_id'].unique())] \
        .to_file(tb_env.tmp_dir / "flood_affected_homesteads.geojson", driver="GeoJSON")

    ## Routes of all flood affected homesteads under normal conditions
    comparison.get_routes(normal, od_pairs=flood_affected) \
        .to_file(tb_env.tmp_dir / "flood_affected_normal_routes.geojson", driver="GeoJSON")

    ## Routes of all flood affected homesteads under flood conditions
    comparison.get_routes(flood, od_pairs=flood_affected) \
        .to_file(tb_env.tmp_dir / "flood_affected_flood_routes.geojson", driver="GeoJSON")
