More Data
=========
The package goal's is to provide a framework with high extensability for data enrichments. 

Installation
------------

Install the ``more-data`` package:
    - ``apt install libspatialindex-dev``
    - ``pip install moredata``


Example Use
-----------

To run the examples, you need to use the following commands on the Linux terminal:

The first step is to clone/download the repository and open the project folder in the terminal. After that, execute this code to install all the necessary requirements:

.. code-block:: bash
    
    $ pip install moredata
    $ pip install jupyter-notebook

Then go to examples directory and open a new jupyter-notebook in examples directory:

.. code-block:: bash

    $ cd examples/

If you want to run elasticsearch or SQL example you should have installed docker or have elasticsearch/MySQL in your machine, then:

.. code-block:: bash
    $ cd examples/
    $ cd elasticsearch_connector
    $ docker-compose up

These commands above should be used befores using sql connector.


