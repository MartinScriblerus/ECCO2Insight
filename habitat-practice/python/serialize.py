import numpy as np

def serialize(data):
    if isinstance(data, type):
        return {"py/numpy.type": data.__name__}
    if isinstance(data, np.integer):
        return {"py/numpy.int": int(data)}
    if isinstance(data, np.float):
        return {"py/numpy.float": data.hex()}