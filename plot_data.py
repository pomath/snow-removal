import matplotlib.pyplot as plt
import numpy as np
import datetime

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

newstart = datetime.date(2009, 2, 1)
newind = x.index(newstart)


x_ = np.arange(0, len(y), 1)
y = y[newind:]
x = x[newind:]
x_= x_[newind:]
p = np.poly1d(np.polyfit(x_, y, 2))
yearrange = (x[0].year, x[-1].year)
summers = [(datetime.date(yr, 12, 1), datetime.date(yr+1, 3, 1)) for yr in range(yearrange[0] - 1, yearrange[1] + 1)]
for summ in summers:
    if summ[0] not in x:
        ind1 = 0
        ind2 = x.index(summ[1])
    elif summ[1] not in x:
        ind1 = x.index(summ[0])
        ind2 = len(x) -1
    else:
        ind1 = x.index(summ[0])
        ind2 = x.index(summ[1])
    winter, = plt.plot(x[ind1:ind2], np.ones((ind2-ind1,)) * min(y[ind1:ind2]), 'r-')
dt = x[0] - datetime.date(x[0].year, 1, 1)

phaseShift = np.pi / (dt.days)
avgSNR = plt.scatter(x,y, s=0.5)
fit, = plt.plot(x, p(x_) -np.cos(2 * np.pi * x_ / 365))
ax = plt.gca()
plt.xlabel('Date')
plt.ylabel('SNR')
plt.title(r'MIN0 $40^{\circ} - 50^{\circ}$ Average L2 SNR')
ax.set_xlim([x[0], x[-1]])
ax.set_ylim([37.5, 41])
plt.legend([avgSNR, fit, winter], ['Average SNR', 'Fit', 'Summer Min'], loc='best')
plt.savefig('averages.eps', format='eps', dpi=1000)
