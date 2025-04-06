import os
import numpy as np

class DataInfo():
    """
    Stores information about the curves stored a specified directory data_dir
    """
    def __init__(self, data_dir, min_x):
        """
        data_dir : str
            directory where data is stored
        
        min_x : float
            Minimum value of scaler for maximum x-value
        """
        self.data_dir = data_dir
        self.scales = np.load(f"{data_dir}/scales.npy")
        dataset_names = set()
        for f in os.listdir(data_dir):
            if f == "scales.npy": continue
            splitter = '_MDS_0'
            if splitter in f:
                dataset_name = f.split(splitter)[0]
                dataset_names.add(dataset_name)
        self.dataset_names = sorted(dataset_names)
        self.max_x = round(self.scales[-1])
        self.min_x = min_x
