import numpy as np

if __name__ == '__main__':
    with open('averages.snr') as f:
        f.readline()
        for line in f:
            tmp = line.split()
            
