from setuptools import setup, find_packages

install_requires = [
    "requests"
    "h3"
    "pandas"
    "numpy"
    "elasticsearch"
]

docs_requires = [
    "sphinx"
    "sphinx-rtd-theme"
    "jinja2"
    "sphinxcontrib-napoleon"
]

setup(
    name = "enrichment"
    version = '0.1'
    packages = find_packages(where='.')
    python_requires=">=3.6"
    install_requires = install_requires
    extras_require={
        "develop": install_require + docs_require,
        "docs": docs_require,
    },
)