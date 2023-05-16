import os

__all__ = ["available", "get_path"]

_module_path = os.path.dirname(__file__)
_available_csv = {
    "airbnb-berlin-main": "./airbnb/airbnb-berlin-main.csv",
    "airbnb-berlin-host": "./airbnb/airbnb-berlin-host.csv",
    "airbnb-berlin-extra": "./airbnb/airbnb-berlin-extra.csv",
}
available = list(_available_csv.keys())


def get_path(dataset):
    if dataset in _available_csv:
        return os.path.abspath(os.path.join(_module_path, _available_csv[dataset]))
    else:
        msg = "The dataset '{data}' is not available. ".format(data=dataset)
        msg += "Available datasets are {}".format(", ".join(available))
        raise ValueError(msg)
