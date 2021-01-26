More Data
=========

Its goal is to provide a framework with high extensability for data enrichments. 
The documentation page is in `docs.zip`, for now.

Installation
------------

Install the ``more-data`` package:
    apt install libspatialindex-dev
    pip install moredata


Example Use
-----------

To run the examples, you need to use the following commands on the Linux terminal:

The first step is to clone/download the repository and open the project folder in the terminal. After that, execute this code to install all the necessary requirements:

.. code-block:: bash
    
    $ pip3 install -r requirements.txt


Then go to examples directory and run the chosen example:

.. code-block:: bash

    $ python3 api-connector/api-ibge.py


Reminder
~~~~~~~~
- Elasticsearch Examples in this repository it's only for show how the components interact because there are a lot of data used that you probably doesn't have.
- If you want to run the elasticsearch examples, run the docker container:

.. code-block:: bash

    $ docker run -d -p 9200:9200 -p 9300:9300 --name elasticsearch-7.6 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.6.2
