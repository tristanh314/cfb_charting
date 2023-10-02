import numpy as np

data_array = np.loadtxt(fname="utah_florida_raw.csv",
                          delimiter=",",
                          dtype=str,)
print(data_array.head())