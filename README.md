## tebetebe: python routing analysis with OSRM and OpenStreetMap

[tebetebe](https://github.com/1papaya/tebetebe) is a Python API to compile, serve, and query routable networks using the [Open Source Routing Machine](https://project-osrm.org) (OSRM) and [OpenStreetMap](https://openstreetmap.org) data, and provides a framework for routing analysis using these networks.

*tebetebe* makes it easy to compile a custom routing "Scenario" by abstracting OSRM executables into a pythonic API, and allows for accurate, reproducible, and *readable* routing analysis to be developed.

Examples of routing analysis include:
* accessibility analysis (*how far away are residents from social services?*)
* vulnerability analysis (*if a bridge were to collapse, who would be affected?*)
* hitchhiking analysis (*which highway onramps are likely to have the most traffic?*)

### Installation

1. **Install osrm-backend binaries**

   * See the [osrm-backend wiki for instructions](https://github.com/Project-OSRM/osrm-backend/wiki/Building-OSRM) on how to build and install the binaries from source
   * osrm-backend Docker images are currently not supported for use with tebetebe
   
2. **Clone tebetebe source code and install**

   ```shell
     git clone https://github.com/1papaya/tebetebe.git
     python3 setup.py install
   ```
   
### Documentation

* [Examples](https://1papaya.github.io/tebetebe/#examples)
* [API Documentation](https://1papaya.github.io/tebetebe/#api-documentation)
   
### Simple Scenario Example

Calculate the route from Mbabane to Simunye using the default walking scenario. Check out the [Documentation](https://1papaya.github.io/tebetebe) for more examples!

```python
import tebetebe as tb
from tebetebe.profiles import foot

tb_env = tb.Environment(tmp_dir="./tmp/simple_scenario")

mbabane = (31.1367, -26.3054)
simunye = (31.9274, -26.2108)

## Initialize scenario ising eSwatini GeoFabrik extract and default foot profile
scenario = tb_env.Scenario("./swaziland-latest.osm.pbf", foot)

## Run scenario and calculate route
with scenario() as api:
    route = api.simple_route(simunye, mbabane)

    duration = route['routes'][0]['duration'] / 60
    distance = route['routes'][0]['distance'] / 1000

    print("Walking from Simunye to Mbabane")
    print(" Duration: {:.2f} minutes".format(duration))
    print(" Distance: {:.2f} km".format(distance))
```
