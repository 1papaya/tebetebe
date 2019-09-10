from tebetebe.analysis import ParallelScenarios, RouteComparison
import tebetebe as tb

queries = {
    "homesteads": """
       node(6750683291)->.crossing;
         ( way(around.crossing:8000)["building"];);
       out center;
    """,
    "schools": """(way(718997017); way(721959090);); out center;"""
}

tb_env = tb.Environment(tmp_dir="./tmp/scenario_comparison",
                        overwrite=False, verbose=False)

## Get route network, origins, and destinations from Overpass
highways = tb_env.RouteNetwork("./tmp/swaziland-latest.osm.pbf", name="swazi")
origins = tb_env.POIDataset.from_overpass(queries["homesteads"], name="homesteads")
dests = tb_env.POIDataset.from_overpass(queries["schools"], name="schools")

## Normal & Flood scenarios. Pass along an extra parameter to osrm-routed
## so that the max duration table size is enough for all origin:dest pairs
routed_args = {"max_table_size": len(origins) * len(dests) + 1}

normal = tb_env.Scenario(highways, "./profiles/walk_normal.lua",
                         routed_args=routed_args, name="normal")
flood = tb_env.Scenario(highways, "./profiles/walk_flood.lua",
                        routed_args=routed_args, name="flood")

## Run normal and flood scenarios in parallel
parallel_scenarios = ParallelScenarios(normal, flood)

with parallel_scenarios as scenarios:
    ## Compare origin:dest routes
    comparison = RouteComparison(origins, dests)

    ## Routes that are different between scenarios
    flood_affected = comparison.get_difference(normal, flood)

    ## Point dataframe of all homesteads who are flood affected
    origins[origins.index.isin(flood_affected['origin_id'].unique())] \
        .to_file(tb_env.tmp_dir / "flood_affected_homesteads.geojson", driver="GeoJSON")

    ## Routes of all flood affected homesteads under normal conditions
    comparison.get_routes(normal, od_pairs=flood_affected) \
        .to_file(tb_env.tmp_dir / "flood_affected_normal_routes.geojson", driver="GeoJSON")

    ## Routes of all flood affected homesteads under flood conditions
    comparison.get_routes(flood, od_pairs=flood_affected) \
        .to_file(tb_env.tmp_dir / "flood_affected_flood_routes.geojson", driver="GeoJSON")
