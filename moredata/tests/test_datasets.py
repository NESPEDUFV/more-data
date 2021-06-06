from moredata.datasets import get_path
from geopandas import GeoDataFrame, points_from_xy
import pandas as pd

import pytest


@pytest.mark.parametrize(
    "test_dataset", ["airbnb-berlin"]
)

def test_read_paths(test_dataset):
    df = pd.read_csv(get_path(test_dataset), low_memory=False)
    assert isinstance(GeoDataFrame(df, geometry=points_from_xy(df.latitude, df.longitude)), GeoDataFrame)

