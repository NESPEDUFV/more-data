MoreData
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/gegen07/more-data/main?labpath=examples)[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1yqE31Q_lEHyvSQrogFQHX8Qk8ZHK0fjP?usp=sharing)
=========



The package goal's is to provide a framework with high extensability for data enrichments. 

Installation
------------

Install the ``more-data`` package:

    $ apt install libspatialindex-dev
    $ pip install moredata


Example Use
-----------

To run the examples, you need to use the following commands on the Linux terminal:

The first step is to clone/download the repository and open the project folder in the terminal. After that, execute this code to install all the necessary requirements:
    
    $ pip install moredata
    $ pip install jupyter-notebook

Then go to examples directory and open a new jupyter-notebook in examples directory:

    $ cd examples/

If you want to run elasticsearch or SQL example you should have installed docker or have elasticsearch/MySQL in your machine, then:

    $ cd examples/
    $ cd elasticsearch_connector
    $ docker-compose up

These commands above should be used befores using sql connector.

## Cite

```
@inproceedings{
    10.1145/3474717.3484210,
    author = {Figueiredo, Leonardo J. A. S. and dos Santos, Germano B. and Souza, Raissa P. P. M. and Silva, Fabr\'{\i}cio A. and Silva, Thais R. M. Braga},
    title = {MoreData: A Geospatial Data Enrichment Framework},
    year = {2021},
    isbn = {9781450386647},
    publisher = {Association for Computing Machinery},
    address = {New York, NY, USA},
    url = {https://doi.org/10.1145/3474717.3484210},
    doi = {10.1145/3474717.3484210},
    booktitle = {Proceedings of the 29th International Conference on Advances in Geographic Information Systems},
    pages = {419–422},
    numpages = {4},
    keywords = {geospatial data, semantic enrichment, framework},
    location = {Beijing, China},
    series = {SIGSPATIAL '21}
} 
```
