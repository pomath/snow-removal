'''
Finds the average SNR for L2 at specified elevation angle.

usage:
python snow_removal.py elevation_file azimuth
'''


import matplotlib.pyplot as plt
import numpy as np
import sys

def make_sats():
    '''
    Creates an empty dictionary for each GPS satellite.
    '''
    data = dict([])
    allsats = ['G{:02}'.format(num) for num in range(1, 33)]
    for sat in allsats:
        data[sat] = []
    return data


def load_data(data_file):
    '''
    input:
    data_file = *.sn1/sn2/ele/azi

    output:
    data = dict with times and values for each satellite.
    '''
    data = make_sats()
    with open(data_file, 'r') as f:
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
                data[sats[nrec]].append([float(tmp1[0]), float(tmp2[nrec])])
    return data


def combine_snr_elev(elev, sn2, stn):
    '''
    inputs:
    elev = dict with 2d array of [time, elevation]
    sn2 = dict with 2d array of [time, sn2]
    stn = string with sattelite name

    output:
    snrvselev = array with [elev, sn2]
    '''
    snrvselev = [(x[1], y[1]) for x, y in zip(elev[stn], sn2[stn])]
    return snrvselev


def isolate_data(snrvselev, elev_range):
    '''
    Isolates the data between certain values of elevation for averaging

    input:
    snrvselev = list with (elevation, snr)
    elev_range = tuple with (low elevation, high elevation)

    output:
    trimmed_snrvselev = list with (elevation, snr) between elev range.
    '''
    trimmed_snrvselev = [x for x in snrvselev 
                         if elev_range[0] <= x[0] <= elev_range[1]]
    return trimmed_snrvselev


def average_SNR(trimmed_snrvselev):
    '''
    Averages the SNR data

    input:
    trimmed_snrvselev = snr data between a certain range of elevation.

    output:
    avg_snr = averaged snr data
    '''
    snr_data = [x[1] for x in trimmed_snrvselev]
    avg_snr = float(sum(snr_data)) / max(len(snr_data), 1)
    return avg_snr

def parse_args(args):
    '''
    input:
    command line args

    output:
    stn_day = station name and day eg. min00130
    '''

    return str(args[1])

if __name__ == '__main__':
    stn = parse_args(sys.argv)
    azimuth = load_data(stn + '.azi')
    elev = load_data(stn + '.ele')
    sn2 = load_data(stn + '.sn2')
    snrvselev = combine_snr_elev(elev, sn2, 'G01')
    trimmed_snrvselev = isolate_data(snrvselev, (40.0, 50.0))
    avg_snr = average_SNR(trimmed_snrvselev)
    print(avg_snr)
