from setuptools import setup, find_packages
import os

# get all data dirs in the datasets module
data_files = []

for item in os.listdir("moredata/datasets"):
    print("")
    if not item.startswith("__"):
        if os.path.isdir(os.path.join("moredata/datasets/", item)):
            data_files.append(os.path.join("datasets", item, "*"))

if os.environ.get("READTHEDOCS", False) == "True":
    INSTALL_REQUIRES = []
    DOCS_REQUIRES = []
    dependencies = []
    elasticsearch = []
    sql = []
    json = []
    osm = []
else:
    dependencies = [
        "requests>=2.31",
        "Rtree>=1.2",
        "pyproj>=3.6",
        "geopy>=2.4",
        "pandas>=2.2",
        "numpy>=1.26",
        "shapely>=2",
    ]

    elasticsearch = [
        "elasticsearch>=8",
    ]

    sql = [
        "SQLAlchemy>=2",
        "PyMySQL>=1.1",
    ]

    json = ["h3>=4"]

    osm = [
        "osm2geojson>=0.2",
        "dask_geopandas>=0.4",
        "geopandas>=1.0",
    ]

    DOCS_REQUIRES = [
        "sphinx==2.4.0",
        "sphinx-rtd-theme==0.4.3",
        "jinja2==2.11.1",
        "sphinxcontrib-napoleon==0.7",
    ]

setup(
    name="moredata",
    url="https://https://github.com/NESPEDUFV/more-data",
    download_url="https://github.com/NESPEDUFV/more-data/archive/v0.2.6.tar.gz",
    version="0.3.0",
    packages=find_packages(where="."),
    python_requires=">=3.10",
    install_requires=dependencies + osm,
    extras_require={
        "elasticsearch": elasticsearch,
        "sql": sql,
        "h3": json,
    },
    # extras_require={
    #     "complete": dependencies + elasticsearch + sql + json + osm,
    #     "osm": dependencies + osm,
    #     "elasticsearch": dependencies + elasticsearch,
    #     "sql": dependencies + sql,
    #     "json": dependencies + json,
    #     "develop": dependencies + DOCS_REQUIRES + elasticsearch + sql + json + osm,
    #     "docs": DOCS_REQUIRES,
    # },
)
