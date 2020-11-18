import pandas as pd
import os
from scipy.fftpack import fftfreq, fft
import numpy as np
import matplotlib.pyplot as plt


def _check_folder(folder):
    if folder != 'Results':
        raise Exception('Module not called in results folder')
    else:
        return


def _open_data():
    data = pd.read_csv('table.txt', sep='\t')[4000:]    # Need to update to something more rigorous
    return data


class distancePlot:

    def __init__(self):
        dirpath = os.getcwd()
        foldername = os.path.basename(dirpath)
        _check_folder(foldername)
        self.walk = os.walk(dirpath)    # Generator for moving through the results directory
        self.max_freqs_small = []     # Initialise empty list to fill with the frequency values
        self.max_freqs_large = []
        self.distances = []     # Distances corresponding to the frequencies

    def _populate_lists(self):

        self.data = self._get_data()
        small, large = self._FT()
        max_small, max_large = self.find_max(small, large)
        self.max_freqs_small.append(max_small)
        self.max_freqs_large.append(max_large)

        dist = self._get_distance()

        self.distances.append(dist)

        self._populate_lists()

    def find_max(self, small, large):

        small_range = small[small['freq'] < 1e9]
        small_range = small[1e6 < small['freq']]
        large_range = large[large['freq'] < 1e9]
        large_range = large[1e6 < large['freq']]

        max_small = small_range['freq'].iloc[small_range['intens'].idxmax()]
        max_large = large_range['freq'].iloc[large_range['intens'].idmax()]

        return max_small, max_large

    def _get_distance(self):
        num = os.path.basename(os.getcwd())[-1]
        file = open('disk{}.mx3'.format(num))
        lines = file.readlines()
        file.close()
        gap = lines[5][7:-2]
        return gap

    def _FT(self):

        f_s = len(self._t) / self._t.iloc[-1]
        small = fft(list(self._mx2))
        large = fft(list(self._mx1))

        small_F = fftfreq(len(self._mx2)) * f_s
        large_F = fftfreq(len(self._mx1)) * f_s

        data_small = pd.DataFrame({'intens': np.abs(small), 'freq': small_F})
        data_large = pd.DataFrame({'intens': np.abs(large), 'freq': large_F})

        return data_small, data_large

    def plot(self):

        plt.scatter(self.distances, self.max_freqs_small, label='Small Disk')
        plt.scatter(self.distances, self.max_freqs_large, label='Large Disk')

        plt.savefig('Frequencies against distance')

        plt.show()
        return

    def _get_data(self):
        root, dirs, files = next(self.walk, ['done', None, None])
        if 'table.txt' in files:
            os.chdir(root)
            data = _open_data()
            return data
        elif root == 'done':
            self.plot()
        else:
            self._get_data()

    @property
    def _t(self):
        return self.data['# t (s)']

    @property
    def _mx(self):
        return self.data['mx ()']

    @property
    def _mx1(self):
        return self.data['m.region1x ()']

    @property
    def _mx2(self):
        return self.data['m.region2x ()']
