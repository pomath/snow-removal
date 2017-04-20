import numpy as np
import pickle
import subprocess


class Data:
    '''
    A set of routines that reads in the teqc +plot
    format into a python data structure.
    The input is a +plot file, currently there are
    no guards against reading in a bad file.
    '''
    __slots__ = ['data', 'dataFile', 'saveName',
                 'found', 'prefix']

    def __init__(self, dataFile):
        self.dataFile = dataFile
        self.prefix = self.dataFile[:-12]
        self.saveName = (self.prefix +
                         self.dataFile[-12:-4] +
                         self.dataFile[-3:] +
                         '.pickle')
        self.data = self.makeSats
        self.fileExists(self.saveName)
        if self.found.returncode == 0:
            print('Loading pickle:', self.saveName)
            self.loadPickle()
        else:
            print('Making data and saving:', self.saveName)
            self.load_data()

    def fileExists(self, fileName):
        self.found = subprocess.run(["ls", fileName.encode('ascii')],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)

    @property
    def makeSats(self):
        '''
        Creates an empty dictionary for each GPS satellite.
        '''
        data = dict([])
        allsats = ['G{:02}'.format(num) for num in range(1, 33)]
        for sat in allsats:
            data[sat] = []
        return data

    def load_data(self):
        '''
        Opens up the +plot file and reads line by line
        updating the epoch and measurement.
        '''
        with open(self.dataFile, 'r') as f:
            f.readline()
            hdr = f.readline()
            # read 2 lines
            for line1 in f:
                line2 = next(f)
                tmp1 = line1.split()
                tmp2 = line2.split()
                nsats = int(tmp1[1])
                if nsats != -1:
                    sats = tmp1[2:]
                else:
                    sats = sats
                    nsats = len(sats)
                # parse the stations and append data
                for nrec in range(nsats):
                    self.data[sats[nrec]].append([float(tmp1[0]),
                                                  float(tmp2[nrec])])
        self.savePickle()

    def savePickle(self):
        with open(self.saveName, 'wb') as f:
            pickle.dump(self.data, f, pickle.HIGHEST_PROTOCOL)

    def loadPickle(self):
        with open(self.saveName, 'rb') as f:
            self.data = pickle.load(f)

if __name__ == '__main__':
    test = Data('test/rob40010.azi')
