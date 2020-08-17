import os
import sys
sys.path.insert(0, os.path.abspath('../../'))

from enrichment.utils.osm_downloader import OSM_util
import csv
import pandas as pd

if __name__ == "__main__":
    osm = OSM_util()
    place_id = osm.get_place_ID("Brasil")
    print(place_id)
    key = "tourism"
    value = "museum"

    query = """
    [out:json];
    area(%s)->.searchArea;
    (
        node[%s=%s](area.searchArea);
        way[%s=%s](area.searchArea);
        relation[%s=%s](area.searchArea);
    );
        out geom;
    >;
    out skel qt;
    """ % (place_id, key, value, key, value, key, value)

    print(key, value)

    df = osm.get_places("Brasil", key, value, query = query)
    df.to_csv("../../data/output/osm/{}-{}.csv".format(key, value))