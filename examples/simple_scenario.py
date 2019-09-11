from tebetebe.profiles import foot
import tebetebe as tb

tb_env = tb.Environment(tmp_dir="./tmp/simple_scenario")

mbabane = (31.1367, -26.3054)
simunye = (31.9274, -26.2108)

## Initialize scenario ising eSwatini GeoFabrik extract and
## default foot profile
scenario = tb_env.Scenario("./tmp/swaziland-latest.osm.pbf", foot)

## Run scenario
with scenario() as api:
    ## Query OSRM HTTP `simple_route` service to calculate route
    route = api.simple_route(simunye, mbabane)

    duration = route['routes'][0]['duration'] / 60
    distance = route['routes'][0]['distance'] / 1000

    print("Walking from Simunye to Mbabane")
    print(" Duration: {:.2f} minutes".format(duration))
    print(" Distance: {:.2f} km".format(distance))
