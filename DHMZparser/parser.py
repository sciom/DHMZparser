import numpy as np

class DHMZdata():
    def __init__(self, datafile):
        self.datafile = datafile

    def read_data(self):
        with open(self.datafile, 'r') as f:
            data = f.readlines()
        return data

        