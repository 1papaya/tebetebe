import tebetebe as tb

tb_env = tb.Environment(tmp_dir="./tmp/simple_scenario",
                        overwrite=False, verbose=False)

mbabane = (31.1367, -26.3054)
simunye = (31.9274, -26.2108)

## Query Overpass API for all ways with "highway" attribute inside eSwatini
highways = tb_env.RouteNetwork \
           .from_overpass("""
                area[name="eSwatini"];
                  (way["highway"](area););
                out meta; >; out skel qt;""",
                          name="swazi")

profile = tb_env.RoutingProfile("./profiles/walk.lua")

## Initialize Scenario
scenario = tb_env.Scenario(highways, profile)

## Run scenario
with scenario() as api:
    route = api.simple_route(simunye, mbabane)

    duration = route['routes'][0]['duration'] / 60
    distance = route['routes'][0]['distance'] / 1000

    print("Walking from Simunye to Mbabane")
    print(" Duration: {:.2f} minutes".format(duration))
    print(" Distance: {:.2f} km".format(distance))
