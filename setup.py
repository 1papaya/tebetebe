import setuptools

setuptools.setup(
    name="tebetebe",
    version="0.0.1",
    author="1papaya",
    author_email="",
    description="Routing analysis with OSM",
    url="https://github.com/1papaya/tebetebe",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        "osrm",
        "geojson",
        "geopandas",
        "overpass",
        "sh"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: MIT License",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires='>=3.6',
)
