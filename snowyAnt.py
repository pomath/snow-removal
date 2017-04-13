'''
'''

from multiprocessing import Pool
from snowyPrep import snowyPrep
from snowyStation import snowyStation


if __name__ == '__main__':
    files = [('rob4', '2013_001', 'test/'),
             ('rob4', '2013_002', 'test/'),
             ('rob4', '2013_003', 'test/'),
             ('rob4', '2013_004', 'test/')]
    snowyPrep(*files[0])
#    with Pool(6) as p:
#        p.starmap(snowyPrep, files)
