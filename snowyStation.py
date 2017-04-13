'''
Finds the average SNR for L2 at specified elevation angle.

usage:
python snow_removal.py elevation_file azimuth
'''

import matplotlib.pyplot as plt
import numpy as np
import sys
from snowyData import snowyData
from snowyPrep import snowyPrep

class snowyStation(snowyData):
    '''
    '''
    __slots__ = ['SNRvsElev', 'plotFP', 'azimuth',
                 'elevation', 'SNR', 'SATS',
                 'eleRange', 'avgSNR', 'stdSNR',
                 'args']

    def __str__(self):
        return '{:.4}'.format(self.avgSNR)

    def __repr__(self):
        return '{:.4}'.format(self.avgSNR)

    def __init__(self, station='min0', date='2008_001',
                 path='plot_files/'):
        self.args = (station, date, path)
        prep = snowyPrep(*self.args)
        self.SNRvsElev = dict([])
        self.plotFP = path + station + date[-3:] + '0'
        self.azimuth = snowyData(self.plotFP + '.azi').data
        self.elevation = snowyData(self.plotFP + '.ele').data
        self.SNR = snowyData(self.plotFP + '.sn2').data
        prep.removeOthers()
        self.SATS = [key for key in self.elevation]
        self.eleRange = (40, 50)
        self.combineSNRElev()
        self.isolateData()
        print(self.avgSNR)

    def combineSNRElev(self):
        for key in self.SATS:
            self.SNRvsElev[key] = [(x[1], y[1]) for x, y in zip(self.elevation[key], self.SNR[key])]

    def isolateData(self):
        trimmed_snrvselev = dict([])
        snr_data = np.array([])
        for key in self.SATS:
            trimmed_snrvselev[key] = [x for x in self.SNRvsElev[key]
                                      if self.eleRange[0] <= x[0] <= self.eleRange[1]]
        for key in self.SATS:
            snr_data = np.append(snr_data, [x[1] for x in trimmed_snrvselev[key]])
        self.avgSNR = float(sum(snr_data)) / max(len(snr_data), 1)
        self.stdSNR = np.std(snr_data)


if __name__ == '__main__':
    '''
    '''
    test = snowyStation('min0', sys.argv[1], './plot_files/')
    print(test, test.stdSNR)
