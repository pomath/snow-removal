'''
'''
from multiprocessing import Pool
from .Prep import Prep
from .Station import Station
from .Plot import Plot
import matplotlib.pyplot as plt
import numpy as np
import pickle
import os

def getSNR(st, yr, pa):
    s = Station(st, yr, pa)
    return [s.date, s.avgSNR]

class Ant:
    '''
    station = 'uthw'
    year = ['2013', '2014', '2015', '2016']
    path = 'DATA/'
    days = list(range(1, 365))
    '''
    def __init__(self, station, year, path, days):
        days = ['{:03}'.format(x) for x in days]
        savename = station + '.pickle'
        files = [(station, yr + '_' + d, path + yr + '/')  for yr in year for d in days]
        if not os.path.isfile(savename):
            print('Creating results list...')
            with Pool(6) as p:
                results = p.starmap(getSNR, files)

            with open(savename, 'wb') as f:
                pickle.dump(results, f, pickle.HIGHEST_PROTOCOL)
        else:
            print('Loading results.pickle')
            with open(savename, 'rb') as f:
                results = pickle.load(f)

        results = [row for row in results if -1.0 not in row]
        dates = [x[0] for x in results]
        SNR = [x[1] for x in results]
        print('Plotting...')
        plots = Plot(dates, SNR, station)
        plots.plotIt()
        plots.plotSummers()
        plt.show()
