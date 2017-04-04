'''
Finds the average SNR for L2 at specified elevation angle.

usage:
python snow_removal.py elevation_file azimuth
'''

import matplotlib.pyplot as plt
import numpy as np
import sys
from GPSData import GPSData
import subprocess
class snowyPrep:
    '''
    '''
    __slots__ = ['rawFP', 'zipFP', 'obsFP',
                 'runTEQC', 'runCRX2RNX']

    def __init__(self, station='min0', date='2008_001',
                 path='plot_files/'):
        self.rawFP = (path + date + '/' +
                       station + date[-3:] +
                       '0.' + date[2:4])
        self.zipFP = self.rawFP + 'd.Z'
        self.zipFP = self.rawFP + 'o'

    def TEQC(self):
        '''
        '''
        self.runTEQC = subprocess.run(["./teqc"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    def CRX2RNX(self):
        '''
        '''
        self.runCRX2RNX = subprocess.run(["./CRX2RNX"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    def failed(self):
        if self.runCRX2RNX.returncode or self.runTEQC.returncode:
            print('Prep failed for ' + self.rawFP)


class snowyStation(GPSData):
    '''
    '''
    __slots__ = ['SNRvsElev', 'plotFP', 'azimuth',
                 'elevation', 'SNR', 'SATS',
                 'eleRange', 'avgSNR', 'stdSNR']

    def __str__(self):
        return '{:.4}'.format(self.avgSNR)

    def __repr__(self):
        return '{:.4}'.format(self.avgSNR)

    def __init__(self, station='min0', date='2008_001',
                 path='plot_files/'):
        self.SNRvsElev = dict([])
        self.plotFP = path + date + '/' + station + date[-3:] + '0'
        self.azimuth = GPSData(self.plotFP + '.azi').data
        self.elevation = GPSData(self.plotFP + '.ele').data
        self.SNR = GPSData(self.plotFP + '.sn2').data
        self.SATS = [key for key in self.elevation]
        self.eleRange = [40, 50]
        self.combineSNRElev()
        self.isolateData()

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
