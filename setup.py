from setuptools import setup, find_packages
import os

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
        "requests==2.28.2",
        "Rtree==1.0.1",
        "pyproj==3.5.0",
        "geopy==2.0.0",
        "pandas>=1.0.1",
        "numpy>=1.18.1",
        "shapely>=1.8",
    ]

    elasticsearch = [
        "elasticsearch>=7.17.0",
    ]

    sql = [
        "SQLAlchemy==1.4.37",
        "PyMySQL==0.10.0",
    ]

    json = ["h3==3.4.3"]

    osm = [
        "osm2geojson==0.1.27",
        "dask_geopandas==0.2.0",
        "geopandas>=0.10.2",
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
    download_url="https://github.com/NESPEDUFV/more-data/archive/v0.2.0.tar.gz",
    version="0.2.0",
    packages=find_packages(where="."),
    python_requires=">=3.8",
    install_requires=dependencies,
    extras_require={
        "complete": dependencies + elasticsearch + sql + json + osm,
        "osm": dependencies + osm,
        "elasticsearch": dependencies + elasticsearch,
        "sql": dependencies + sql,
        "json": dependencies + json,
        "develop": dependencies + DOCS_REQUIRES + elasticsearch + sql + json + osm,
        "docs": DOCS_REQUIRES,
    },
)
