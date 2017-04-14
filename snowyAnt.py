'''
'''

from multiprocessing import Pool
from snowyPrep import snowyPrep
from snowyStation import snowyStation
import numpy as np


if __name__ == '__main__':
    station = 'rob4'
    year = '2016'
    path = 'DATA/' + year + '/'
    days = list(range(1, 6))
    days = ['{:03}'.format(x) for x in days]
    files = [(station, year + '_' + d, path) for d in days]
    
    with Pool(6) as p:
        results = p.starmap(snowyStation, files)


