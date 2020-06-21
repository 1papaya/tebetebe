## tebetebe: python routing analysis with OSRM

[tebetebe](https://github.com/geoDavey/tebetebe) is a Python API to compile, serve, and query routable networks using the [Open Source Routing Machine](https://project-osrm.org) (OSRM) and [OpenStreetMap](https://openstreetmap.org) data, and provides various classes to perform routing analysis using these networks.

*tebetebe* abstracts OSRM executables into a pythonic API, making it easy to generate a custom routing "Scenario" and develop reproducible, readable routing analysis.

### Installation

1. **Install osrm-backend binaries**

   * See the [osrm-backend wiki for instructions](https://github.com/Project-OSRM/osrm-backend/wiki/Building-OSRM) on how to build and install the binaries from source
   * osrm-backend Docker images are currently not supported for use with tebetebe
   
2. (option 1) **Install from pip**

   ```shell
     pip3 install tebetebe
   ```

3. (option 2) **Clone tebetebe source code and install**

   ```shell
     git clone https://github.com/geoDavey/tebetebe.git
     python3 setup.py install
   ```
   
### Documentation

* [Examples](https://geoDavey.github.io/tebetebe/#examples)
* [API Documentation](https://geoDavey.github.io/tebetebe/#api-documentation)
   
### Simple Scenario Example

Calculate the route from Mbabane to Simunye using the default walking scenario. Check out the [Documentation](https://geoDavey.github.io/tebetebe) for more examples!

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
