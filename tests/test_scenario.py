import tebetebe as tb
import unittest

class ScenarioTestCase(unittest.TestCase):
    def setUp(self):
        self.env = tb.Environment(tmp_dir="/tmp/test_scenario", overwrite=True)

        ## Origins / Dests
        self.origins = self.env.POIDataset.from_file("./data/ngwempisi_homesteads.geojson")
        self.dests = self.env.POIDataset.from_file("./data/ngwempisi_schools.geojson")

        ## Route Profile & Route Network
        self.walk_normal = self.env.RoutingProfile("./profiles/walk_normal.lua")
        self.route_network = self.env.OSMDataset("./data/ngwempisi.osm.pbf")

    def ztest_scenario_run_MLD(self):
        ## Scenario
        self.scenario = self.env.Scenario(self.route_network, self.walk_normal,
                                          algorithm="MLD", name="MLD")

        ## Test Compilation
        self.scenario()
        assert self.scenario.path.is_file(), "Scenario not compiled"

        ## Test Scenario HTTP API
        with self.scenario as api:
            assert api.scenario.is_alive() == True, "Scenario not alive after context manager execution"


    def ztest_scenario_run_CH(self):
        self.scenario = self.env.Scenario(self.route_network, self.walk_normal,
                                          algorithm="CH", name="CH")

        ## Test Compilation
        self.scenario()
        assert self.scenario.path.is_file(), "Scenario not compiled"

        ## Test Scenario HTTP API
        with self.scenario as api:
            assert api.scenario.is_alive() == True, "Scenario not alive after context manager execution"

    def test_scenario_nearest(self):
        self.scenario = self.env.Scenario(self.route_network, self.walk_normal, name="normal")

        with self.scenario() as api:
            nearest = api.nearest((0,0), 3)
            
            assert nearest is not None, "Error in ScenarioAPI.nearest"
            assert len(nearest) == 3, "Nearest did not return 3 points"

    def test_scenario_route(self):
        pass

if __name__ == '__main__':
    unittest.main()