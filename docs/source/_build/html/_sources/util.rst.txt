.. _util:

Conversion 
----------

.. py:module:: moredata.utils.util.Converter

.. autofunction:: json_enriched_to_csv

.. autofunction:: csv_to_json


Geodesic Point Buffer 
---------------------

Example
~~~~~~~

Here it's a example of use of point bufferization with 500 meters of radius. After bufferization is saved the result in a file.

.. code-block:: python

    from moredata.utils.util import geodesic_point_buffer

    import json

    DATASETS_DIR = "../datasets/"
    USER_DATA = DATASETS_DIR + "user_profile_17092019_preprocessed.json"

    USER_PROJECT_DATA = "./data/amenity-restaurant-0.json"

    with open(USER_PROJECT_DATA) as f:
        data = json.loads(f.read())
        counter = 0
        for d in data:
            for points in d["points_of_interest"]:
                shp = Polygon(geodesic_point_buffer(points["latitude"], points["longitude"], 500)) 
                points["area_point"] = shp.wkt
        with open("./data/amenity-restaurant-0.json", 'w') as outfile:
            json.dump(data, outfile, ensure_ascii=False)

.. py:module:: moredata.utils.util

.. autofunction:: geodesic_point_buffer

