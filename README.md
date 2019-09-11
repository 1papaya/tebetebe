# tebetebe: routing analysis with OSM

[tebetebe](https://github.com/1papaya/tebetebe) is a Python API for the [Open Source Routing Machine](https://project-osrm.org) (OSRM) to compile, serve, and query routable networks using [OpenStreetMap](https://openstreetmap.org) data.

## Installation

1. **Install osrm-backend binaries**

   * See the [osrm-backend wiki for instructions](https://github.com/Project-OSRM/osrm-backend/wiki/Building-OSRM) on how to build and install the binaries from source
   * osrm-backend Docker images are currently not supported for use with tebetebe
   
2. **Clone tebetebe source code and install**

   ```shell
     git clone https://github.com/1papaya/tebetebe.git
     python3 setup.py install
   ```

## [Documentation](https://1papaya.github.io/tebetebe)
   
### Simple Example

Calculate the route from Mbabane to Simunye using a walking scenario. Check out the [Documentation](https://1papaya.github.io/tebetebe) for more examples!

```python
import tebetebe as tb
from tebetebe.profiles import foot

tb_env = tb.Environment(tmp_dir="./tmp/simple_scenario",
                        overwrite=False, verbose=False)

mbabane = (31.1367, -26.3054)
simunye = (31.9274, -26.2108)

## Initialize scenario ising eSwatini GeoFabrik extract and
## osrm-backend default foot profile
scenario = tb_env.Scenario("./swaziland-latest.osm.pbf", foot)

## Run scenario
with scenario() as api:
    ## Query OSRM HTTP `simple_route` service to calculate route
    route = api.simple_route(simunye, mbabane)

    duration = route['routes'][0]['duration'] / 60
    distance = route['routes'][0]['distance'] / 1000

    print("Walking from Simunye to Mbabane")
    print(" Duration: {:.2f} minutes".format(duration))
    print(" Distance: {:.2f} km".format(distance))
```
