:tocdepth: 2

############
tebetebe: routing analysis with OSM
############

`tebetebe <https://github.com/1papaya/tebetebe>`_ is a Python API to compile, serve, and query routable networks using the `Open Source Routing Machine <https://project-osrm.org>`_ (OSRM) and `OpenStreetMap <https://openstreetmap.org>`_ data, and provides a framework for routing analysis using these networks.

Package Overview
********

`tebetebe` makes it easy to compile a custom routing `Scenario` by abstracting OSRM executables into a pythonic API, and provides a wide opporunity to customize these scenarios and run various types of routing analysis.

With the range of customization available in the .lua configuration files, specific accurate and *readable* transportation models can be developed to be fed into other types of analysis.

Examples of routing analysis include: accessibility analysis (`how far away are residents from social services?`), vulnerability analysis (`if a bridge were to collapse, who would be affected?`), and hitchhiking analysis (`which roads are likely to have the most traffic?`)

`tebetebe` also simplifies the routing analysis pipeline by enabling data to be pulled live from the Overpass API and modified programmatically by Osmium. Finally, the package contains various user-contributed classes which automate common tasks in routing analysis, such as isochrones.

Comments, suggestions, and contributions are welcomed!

Installation
************

1. Install `osrm-backend <https://github.com/Project-OSRM/osrm-backend/>`_ binaries
----

  * See the `osrm-backend wiki for instructions <https://github.com/Project-OSRM/osrm-backend/wiki/Building-OSRM>`_ on how to build and install from source.
  * Note that the `osrm-backend` Docker images are not supported for use with tebetebe.

2. Clone `tebetebe <https://github.com/1papaya/tebetebe>`_ source code and install
----
  .. code:: text

     git clone https://github.com/1papaya/tebetebe.git
     python3 setup.py install


*note:* tebetebe will not work on Windows machines

########
Examples
########

Simple Scenario
***************

This example uses the eSwatini GeoFabrik extract and the `default walking profile <https://github.com/Project-OSRM/osrm-backend/blob/master/profiles/foot.lua>`_ to calculate a walking route between Simunye and Mbabane.

.. literalinclude:: ../../examples/simple_scenario.py

.. code-block:: shell
   :caption: Simple Scenario output

    [   INFO] swaziland-latest_foot: Compiling scenario (MLD)
    [WARNING] swaziland-latest_foot: Default foot profile may not be accurate for your use case
    [   INFO] swaziland-latest_foot: Initializing scenario
    [   INFO] swaziland-latest_foot: Ready for requests
    Walking from Simunye to Mbabane
     Duration: 1420.70 minutes
     Distance: 118.39 km

Scenario Comparison
****************

By comparing origin:destination routes between different scenarios, we gain insight about how changing a transportation scenario affects route patterns.

Here, we compare routes calculated by two different Scenarios: a "normal" walking scenario, and a "flood" scenario, to understand the impact of a flooding event on access to local schools in eSwatini. The route network is taken from the eSwatini GeoFabrik extract, and the homesteads (origins) and schools (destinations) are downloaded from the Overpass API.

The "normal"  and "flood" scenarios in this case are both the default walk profile, except that the "flood" scenaro considers nodes with ``ford=yes`` (river crossings), and ways with ``flood_prone=yes`` to be a barrier. Check out their source in `the GitHub repo 
<https://github.com/1papaya/tebetebe/tree/master/examples>`_

.. literalinclude:: ../../examples/scenario_comparison.py

.. code-block:: text
   :caption: Scenario Comparison output

    [   INFO] Downloading POIDataset homesteads
    [   INFO] Downloading POIDataset schools
    [   INFO] normal: Compiling scenario (MLD)
    [   INFO] normal: Initializing scenario
    [   INFO] normal: Ready for requests
    [   INFO] flood: Compiling scenario (MLD)
    [   INFO] flood: Initializing scenario
    [   INFO] flood: Ready for requests


Access Isochrones
***************

Here a route network is extracted from the eSwatini `GeoFabrik extract <http://download.geofabrik.de>`_ and an AccessIsochrone is calculated using the default `car profile <https://github.com/Project-OSRM/osrm-backend/blob/master/profiles/foot.lua>`_. The AccessIsochrone class is provided by the `python-osrm package <https://github.com/ustroetz/python-osrm>`_.

.. literalinclude:: ../../examples/access_isochrones.py

.. code-block:: text
   :caption: Access Isochrones output

    [   INFO] swaziland-latest_car: Compiling scenario (MLD)
    [WARNING] swaziland-latest_car: Default car profile may not be accurate for your use case
    [   INFO] swaziland-latest_car: Initializing scenario
    [   INFO] swaziland-latest_car: Ready for requests

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

tb.OSMDataset
***************

.. automodule:: tebetebe.OSMDataset
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
