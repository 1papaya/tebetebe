import tebetebe as tb
import unittest

class ScenarioTestCase(unittest.TestCase):
    def setUp(self):
        self.env = tb.Environment(tmp_dir="/tmp/test_scenario", overwrite=True, verbose=False)

        ## Origins / Dests
        self.origins = self.env.POIDataset.from_file("./data/ngwempisi_homesteads.geojson")
        self.dests = self.env.POIDataset.from_file("./data/ngwempisi_schools.geojson")

        ## Route Profiles
        self.walk_normal = self.env.RoutingProfile("./profiles/walk_normal.lua")
        self.walk_flood = self.env.RoutingProfile("./profiles/walk_flood.lua")

        ## Route Network
        self.route_network = self.env.OSMDataset("./data/ngwempisi.osm.pbf")

        ## Scenarios
        self.s_normal = self.env.Scenario(self.route_network, self.walk_normal,
                                          name="normal")
        self.s_flood = self.env.Scenario(self.route_network, self.walk_flood,
                                         name="flood")

        ## Delete scenarios so recompiled for each test
        for scenario in [self.s_normal, self.s_flood]:
            if scenario.path.is_file():
                scenario.path.unlink()

    def test_scenario_compile(self):
        tst_scenario = self.s_normal

        tst_scenario()
        assert tst_scenario.path.is_file() == True, "Scenario file does not exist"

    def test_scenario_run(self):
        tst_scenario = self.s_normal

        with tst_scenario() as scn:
            assert scn.process.process.is_alive() == True, "Scenario not alive after context manager execution"

if __name__ == '__main__':
    unittest.main()
