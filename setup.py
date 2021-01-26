from setuptools import setup, find_packages

install_requires = [
    "requests==2.22.0",
    "SQLAlchemy==1.3.18",
    "PyMySQL==0.10.0",
    "h3==3.4.3",
    "osm2geojson==0.1.27",
    "Rtree==0.9.4",
    "pyproj==2.4.2.post1",
    "geopandas==0.7.0",
    "geopy==2.0.0",
    "pandas==1.0.1",
    "numpy==1.18.1",
    "elasticsearch==7.5.1",
    "shapely==1.7.0",
]
docs_requires = [
    "sphinx==2.4.0",
    "sphinx-rtd-theme==0.4.3",
    "jinja2==2.11.1",
    "sphinxcontrib-napoleon==0.7",
]

setup(
    name = "moredata",
    version = '0.1',
    packages = find_packages(where="."),
    python_requires=">=3.6",
    install_requires = install_requires,
    extras_require={
        "develop": install_requires + docs_requires,
        "docs": docs_requires,
    },
)
