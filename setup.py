from setuptools import setup, find_packages
import os

if os.environ.get("READTHEDOCS", False) == "True":
    INSTALL_REQUIRES = []
    DOCS_REQUIRES = []
else: 
    INSTALL_REQUIRES = [
        "requests==2.22.0",
        "SQLAlchemy==1.4.37",
        "PyMySQL==0.10.0",
        "osm2geojson==0.1.27",
        "h3==3.4.3",
        "Rtree==0.9.7",
        "pyproj==2.4.2.post1",
        "geopandas>=0.7.0",
        "geopy==2.0.0",
        "pandas>=1.0.1",
        "numpy>=1.18.1",
        "elasticsearch>=7.5.1",
        "shapely==1.7.0",
    ]

    DOCS_REQUIRES = [
        "sphinx==2.4.0",
        "sphinx-rtd-theme==0.4.3",
        "jinja2==2.11.1",
        "sphinxcontrib-napoleon==0.7",
    ]

setup(
    name="moredata",
    url='https://github.com/gegen07/more-data',
    download_url='https://github.com/gegen07/more-data/archive/v0.1.2.tar.gz',
    version='0.1.2',
    packages=find_packages(where="."),
    python_requires=">=3.6",
    install_requires=INSTALL_REQUIRES,
    extras_require={
        "develop": INSTALL_REQUIRES + DOCS_REQUIRES,
        "docs": DOCS_REQUIRES,
    },
)
