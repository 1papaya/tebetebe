:tocdepth: 2

############
tebetebe: routing analysis with OSM
############

`tebetebe <https://github.com/1papaya/tebetebe>`_ is a Python API to compile, serve, and query routable networks using the `Open Source Routing Machine <https://project-osrm.org>`_ (OSRM) and `OpenStreetMap <https://openstreetmap.org>`_ data, and a framework for routing analysis using these networks.

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

RoutingProfiles referenced by the examples can be found in the `/examples/ folder
<https://github.com/1papaya/tebetebe/tree/master/examples>`_ of the GitHub repo.

Simple Scenario
***************

This example uses the eSwatini GeoFabrik extract and the `default walking profile <https://github.com/Project-OSRM/osrm-backend/blob/master/profiles/foot.lua>`_ to calculate a walking route between Simunye and Mbabane.

.. literalinclude:: ../../examples/simple_scenario.py


.. code-block:: shell
   :caption: Simple Scenario output

    Walking from Simunye to Mbabane
     Duration: 1420.70 minutes
     Distance: 118.39 km

Scenario Comparison
****************

By comparing origin:destination routes between different scenarios, we gain insight about how changing a transportation scenario affects route patterns.

Here, we compare routes calculated by two different Scenarios: a "normal" walking scenario, and a "flood" scenario, to understand the impact of a flooding event on access to local schools in eSwatini. The route network is taken from the eSwatini GeoFabrik extract, and the homesteads (origins) and schools (destinations) are downloaded from the Overpass API.

The "normal"  and "flood" scenarios in this case are both the default walk profile, except that the "flood" scenari considers nodes with ``ford=yes`` (river crossings), and ways with ``flood_prone=yes`` to be a barrier.

.. literalinclude:: ../../examples/scenario_comparison.py

Access Isochrones
***************

Here a route network is extracted from the eSwatini `GeoFabrik extract <http://download.geofabrik.de>`_ and an AccessIsochrone is calculated using the default `car profile <https://github.com/Project-OSRM/osrm-backend/blob/master/profiles/foot.lua>`_. The AccessIsochrone class is provided by the `python-osrm package <https://github.com/ustroetz/python-osrm>`_.

.. literalinclude:: ../../examples/access_isochrones.py

.. figure:: _static/img/mbabane_isochrone.png
   :height: 250px
   :width: 250px

   Result visualized over OSM Carto basemap

^^^^

########
API Documentation
########

tb.Scenario
***************

.. automodule:: tebetebe.Scenario
   :members:
   :undoc-members:
   :show-inheritance:

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

Analysis plugins are classes written on top of the `tebetebe` base classes to automate
routing analysis

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
