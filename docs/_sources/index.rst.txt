:tocdepth: 2

############
tebetebe: routing analysis with OSM
############

`tebetebe <https://github.com/1papaya/tebetebe>`_ is a Python API for the `Open Source Routing Machine <https://project-osrm.org>`_ (OSRM) to compile, serve, and query routable networks using `OpenStreetMap <https://openstreetmap.org>`_ data, and to provide a framework for routing analysis with these networks.

Installation
************

1. Install `osrm-backend <https://github.com/Project-OSRM/osrm-backend/>`_ binaries
----

  * See the `osrm-backend wiki for instructions <https://github.com/Project-OSRM/osrm-backend/wiki/Building-OSRM>`_ on how to build and install from source.
  * Note that the `osrm-backend` Docker images are not supported for use with tebetebe.

2. Clone `tebetebe <https://github.com/1papaya/tebetebe>`_ source code and install
----
  .. code:: shell

     git clone https://github.com/1papaya/tebetebe.git
     python3 setup.py install

^^^^

########
Examples
########

Files referenced by the examples can be found in the `/examples/ folder
<https://github.com/1papaya/tebetebe/tree/master/examples>`_ of the GitHub repo.

Simple Scenario
***************

This example downloads eSwatini highways from the Overpass API and uses the `default walking profile <https://github.com/Project-OSRM/osrm-backend/blob/master/profiles/foot.lua>`_ from `osrm-backend` to calculate a walking route between Simunye and Mbabane.

.. literalinclude:: ../../examples/simple_scenario.py

Scenario Comparison
****************

By comparing origin:destination routes between different scenarios, we gain insight about how changing a transportation scenario affects route patterns.

Here, we route the homesteads in an 8km radius from a river crossing to the local primary and high schools, both in a normal walking scenario and a flood scenario. We then compare the routes between scenarios to determine the homesteads affected by flood and the routes both in normal and flood conditions.

The normal walking scenario in this case is the standard default `walk.lua` from `osrm-backend`. The `walk_flood.lua` is the same scenario except it considers nodes with ford=yes to be a barrier.

.. literalinclude:: ../../examples/scenario_comparison.py

Access Isochrones
***************

Here a route network is extracted from the eSwatini `GeoFabrik extract <http://download.geofabrik.de>`_ an AccessIsochrone is calculated using the `default car profile <https://github.com/Project-OSRM/osrm-backend/blob/master/profiles/foot.lua>`_ from `osrm-backend`.
AccessIsochrone is provided by the `python-osrm package <https://github.com/ustroetz/python-osrm>`_.

.. literalinclude:: ../../examples/access_isochrones.py

.. figure:: _static/img/mbabane_isochrone.png
   :height: 250px
   :width: 250px

   Result visualized over OSM Carto basemap

^^^^

########
API Documentation
########

tb.RouteNetwork
***************

.. automodule:: tebetebe.RouteNetwork
   :members:
   :undoc-members:
   :show-inheritance:

tb.RoutingProfile
***************

.. automodule:: tebetebe.RoutingProfile
   :members:
   :undoc-members:
   :show-inheritance:

tb.Scenario
***************

.. automodule:: tebetebe.Scenario
   :members:
   :undoc-members:
   :show-inheritance:

tb.POIDataset
***************

.. automodule:: tebetebe.POIDataset
   :members:
   :undoc-members:
   :show-inheritance:

tb.Environment
***************

.. automodule:: tebetebe.Environment
   :members:
   :undoc-members:
   :show-inheritance:

tb.OSRM
***************

.. automodule:: tebetebe.OSRM
   :members:
   :undoc-members:
   :show-inheritance:

^^^^

###########
Analysis Plugins
###########

tb.analysis.AccessIsochrone
*********************

.. automodule:: tebetebe.analysis.AccessIsochrone
   :members:
   :undoc-members:
   :show-inheritance:


tb.analysis.ParallelScenarios
*********************

.. automodule:: tebetebe.analysis.ParallelScenarios
   :members:
   :undoc-members:
   :show-inheritance:


tb.analysis.RouteComparison
*********************

.. automodule:: tebetebe.analysis.RouteComparison
   :members:
   :undoc-members:
   :show-inheritance:
