import numpy as np

def deserialize(data):
    if "py/numpy.type" in data:
        return np.dtype(data["py/numpy.type"]).type
    if "py/numpy.int" in data:
        return np.int32(data["py/numpy.int"])
    if "py/numpy.float" in data:
        return np.float64.fromhex(data["py/numpy.float"])