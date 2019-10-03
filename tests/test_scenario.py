import tebetebe as tb
import unittest
import logging
import json

class ScenarioTestCase(unittest.TestCase):
    def setUp(self):
        #logging.getLogger(tb.defaults.LOGGER).setLevel(100) ## Disable logging
        self.env = tb.Environment(tmp_dir="/tmp/test_scenario", overwrite=True,
                                  routed_args={"verbose": True})

        ## Origins / Dests
        self.origins = self.env.POIDataset.from_file("./data/ngwempisi_homesteads.geojson")
        self.dests = self.env.POIDataset.from_file("./data/ngwempisi_schools.geojson")

        ## Route Profile & Route Network
        self.walk_normal = self.env.RoutingProfile("./profiles/walk_normal.lua")
        self.route_network = self.env.OSMDataset("./data/ngwempisi.osm.pbf")

    def test_scenario_run_MLD(self):
        ## Scenario
        scenario = self.env.Scenario(self.route_network, self.walk_normal,
                                          name="test_scenario_run_MLD", algorithm="MLD")

        ## Test Compilation
        scenario()
        assert scenario.path.is_file(), "Scenario not compiled"

        ## Test Scenario HTTP API
        with scenario as scn:
            assert scn.is_alive() == True, "Scenario not alive after context manager execution"


    def test_scenario_run_CH(self):
        scenario = self.env.Scenario(self.route_network, self.walk_normal,
                                     name="test_scenario_run_CH", algorithm="CH")

        ## Test Compilation
        scenario()
        assert scenario.path.is_file(), "Scenario not compiled"

        ## Test Scenario HTTP API
        with scenario as scn:
            assert scn.is_alive() == True, "Scenario not alive after context manager execution"

    def test_scenario_nearest(self):
        scenario = self.env.Scenario(self.route_network, self.walk_normal,
                                     name="test_scenario_nearest")

        with scenario() as scn:
            nearest = scn.api.nearest((0,0), 3)
            print(json.dumps(nearest, indent=2, sort_keys=True))

            assert nearest is not None, "Error in ScenarioAPI.nearest"
            assert len(nearest['waypoints']) == 3, "Nearest did not return 3 points"

    def test_scenario_route(self):
        scenario = self.env.Scenario(self.route_network, self.walk_normal,
                                     name="test_scenario_route")

        waypoints = [self.origins.loc[0, 'geometry'], self.dests.loc[0, 'geometry']]

        with scenario() as scn:
            route = scn.api.route(waypoints)
            print(json.dumps(route, indent=2, sort_keys=True))

            assert route is not None, "Error in ScenarioAPI.route"

if __name__ == '__main__':
    unittest.main()
