'''
download data
make the plot files
load into numpy arrays and save as binaries
'''

import subprocess

class snowyPrep:
    '''
    Used to go from a zipped rinex file to the plot files from TEQC.
    -need to add more checks to make it dummy proof.
    '''
    __slots__ = ['rawFP', 'zipFP', 'obsFP',
                 'crxFP', 'runTEQC', 'runCRX2RNX',
                 'workPath', 'found', 'gzip']

    def __init__(self, station='min0', date='2008_001',
                 path="plot_files/"):
        self._workingDir()
        self.rawFP = (self.workPath + '/' + path
                      +
                      station + date[-3:] +
                      '0.' + date[2:4])
        self.zipFP = self.rawFP + 'd.Z'
        self.navFP = self.rawFP + 'n.Z'
        self.obsFP = self.rawFP + 'o'
        self.crxFP = self.rawFP + 'd'

    def _workingDir(self):
        self.workPath = subprocess.run(["pwd"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.workPath = self.workPath.stdout[:-1]
        self.workPath = self.workPath.decode('ascii')

    def fileExists(self, fileName):
        self.found = subprocess.run(["ls", fileName.encode('ascii')], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    def CRX2RNX(self):
        self.runCRX2RNX = subprocess.run(["./CRX2RNX", self.crxFP], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    def TEQC(self):
        self.runTEQC = subprocess.run(["./teqc", "+qcq", "+plot", self.obsFP], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    def unzip(self, inputFile):
        self.gzip = subprocess.run(["gzip", "-df", inputFile])

    def preProc(self):
        for rawFiles in [self.rawFP, self.navFP]:
            self.fileExists(rawFiles)
            if self.found.returncode:
                print("Didn't find ", rawFiles)
            else:
                self.unzip(rawFiles)
        self.fileExists(self.crxFP)
        if self.found.returncode:
            print("Didn't find ", self.crxFP)
        else:
            self.CRX2RNX(self.crxFP)
        self.fileExists(self.obsFP)
        if self.found.returncode:
            print("Didn't find ", self.obsFP)
        else:
            self.TEQC(self.obsFP)


if __name__ == '__main__':
    test = snowyPrep('rob4', '2005_227', 'DATA/')
    test.fileExists()
