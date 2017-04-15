'''
'''
import matplotlib.pyplot as plt
import numpy as np
import datetime

class Plot:
    '''
    '''
    __slots__ = ['x', 'y', 'name']
    
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name

    def readFile(self):
        '''
        '''
        x = []
        y = np.array([])
        stdev = np.array([])
        with open('averages.snr') as f:
            head = f.readline().split()
            startday = datetime.date(int(head[2]),1,int(head[4]))

            for line in f:
                tmp = line.split()
                days2add = 365 * (int(tmp[0]) - startday.year) + int(tmp[1])
                x.append(startday + datetime.timedelta(days2add))
                y = np.append(y, (float(tmp[2])))
                stdev = np.append(stdev, abs(float(tmp[3])))
        self.x, self.y = x, y

    def shiftStart(self):
        '''
        Shifts the starting date to newstart
        newstart = datetime.date(2009, 2, 1)
        newind = 0 #x.index(newstart)
        y = y[newind:]
        x = x[newind:]
        x_= x_[newind:]
        '''

    def plotFit(self):
        '''
        '''
        x_ = np.arange(0, len(self.y), 1)
        p = np.poly1d(np.polyfit(x_, self.y, 2))
        fit, = plt.plot(self.x, p(x_) - np.cos(2 * np.pi * x_ / 365))

    def plotSummers(self):
        '''
        '''
        x = self.x
        y = self.y
        yearrange = (x[0].year, x[-1].year)
        summers = [(datetime.date(yr, 12, 1), datetime.date(yr+1, 3, 1)) for yr in range(yearrange[0] - 1, yearrange[1] + 1)]
        for summ in summers:
            ind1 = x.index(nearest(x, summ[0]))
            ind2 = x.index(nearest(x, summ[1]))
            if y[ind1:ind2]:
                winter, = plt.plot(x[ind1:ind2], np.ones((ind2-ind1,)) * min(y[ind1:ind2]), 'r-')

    def plotIt(self):
        '''
        '''
        x = self.x
        y = self.y
        miny = min(y) - 1
        maxy = max(y) + 1
        avgSNR = plt.scatter(x,y, s=0.5)
        ax = plt.gca()
        plt.xlabel('Date')
        plt.ylabel('SNR')
        plt.title(self.name + r' $40^{\circ} - 50^{\circ}$ Average L2 SNR')
        ax.set_xlim([x[0], x[-1]])
        ax.set_ylim([miny, maxy])
        #plt.legend([avgSNR, fit, winter], ['Average SNR', 'Fit', 'Summer Min'], loc='best')
        plt.savefig(self.name+'.eps', format='eps', dpi=1000)

def nearest(items, pivot):
    '''
    '''
    return min(items, key=lambda x: abs(x - pivot))
