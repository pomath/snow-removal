'''
download data
make the plot files
load into numpy arrays and save as binaries
'''

import subprocess
from snowyData import snowyData


class snowyPrep:
    '''
    Used to go from a zipped rinex file to the plot files from TEQC.
    -need to add more checks to make it dummy proof.
    '''
    __slots__ = ['rawFP', 'zipFP', 'obsFP', 'navFP',
                 'crxFP', 'runTEQC', 'runCRX2RNX',
                 'workPath', 'found', 'gzip', 'prefix',
                 'path', 'args']

    def __init__(self, station='min0', date='2008_001',
                 path="plot_files/"):
        self.args = (station, date, path)
        self._workingDir()
        self.path = self.workPath + '/' + path
        self.prefix = station + date[-3:] + '0'
        self.rawFP = (self.workPath + '/' + path
                      +
                      station + date[-3:] +
                      '0.' + date[2:4])
        self.zipFP = self.rawFP + 'd.Z'
        self.navFP = self.rawFP + 'n.Z'
        self.obsFP = self.rawFP + 'o'
        self.crxFP = self.rawFP + 'd'
        print("Prepping", self.rawFP)
        self.runPrep()

    def _workingDir(self):
        self.workPath = subprocess.run(["pwd"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.workPath = self.workPath.stdout[:-1]
        self.workPath = self.workPath.decode('ascii')

    def fileExists(self, fileName):
        self.found = subprocess.run(["ls", fileName.encode('ascii')], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    def CRX2RNX(self):
        self.runCRX2RNX = subprocess.run(["./CRX2RNX", "-f", self.crxFP], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    def TEQC(self):
        self.runTEQC = subprocess.run(["./teqc", "+qcq", "+plot", self.obsFP], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    def unzip(self, inputFile):
        self.gzip = subprocess.run(["gzip", "-df", "-k", inputFile])

    def preProc(self):
        for rawFiles in [self.zipFP, self.navFP]:
            self.fileExists(rawFiles)
            if self.found.returncode:
                print("Didn't find ", rawFiles)
            else:
                self.unzip(rawFiles)
        self.fileExists(self.crxFP)
        if self.found.returncode:
            print("Didn't find ", self.crxFP)
        else:
            self.CRX2RNX()
        self.fileExists(self.obsFP)
        if self.found.returncode:
            print("Didn't find ", self.obsFP)
        else:
            self.TEQC()

    def checkFinal(self):
        fileSuffix = ['.azi', '.ele', '.sn2']
        for suff in fileSuffix:
            self.fileExists(self.prefix + suff)
            if (self.found.returncode != 0):
                return 1
        print("Didn't find the plot files, creating them now...")
        return 0

    def runPrep(self):
        self.checkFinal()
        if self.found.returncode != 0:
            self.preProc()

    def toPickle(self):
        fileSuffix = ['.azi', '.ele', '.sn2']
        for f in fileSuffix:
            GPSData(self.prefix + f)

    def removeOthers(self):
        for ext in ['.azi', '.ele', '.d12', '.i12', '.m12', '.m21', '.sn1', '.sn2']:
            removing = subprocess.run(["rm", "-f", self.path + self.prefix + ext], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for f in ['d', 'o', 'n']:
            removing = subprocess.run(["rm", "-f", self.rawFP + f], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

if __name__ == '__main__':
    test = snowyPrep('rob4', '2013_001', 'test/')
    test.removeOthers()
