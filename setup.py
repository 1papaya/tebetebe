import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tebetebe",
    version="0.0.1",
    author="1papaya",
    author_email="1love1papaya@gmail.com",
    description="routing analysis with OSRM",
    long_description_content_type="text/markdown",
    long_description="routing analysis with OSRM",
    url="https://github.com/1papaya/tebetebe",
    packages=setuptools.find_packages(),
    include_package_data=True,
    license="MIT",
    install_requires=[
        "osrm",
        "geojson",
        "geopandas",
        "overpass",
        "sh"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires='>=3.6',
)
