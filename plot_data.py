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


y = y[newind:]
x = x[newind:]
yearrange = (x[0].year, x[-1].year)

summers = [(datetime.date(yr, 12, 1), datetime.date(yr+1, 3, 1)) for yr in range(yearrange[0] - 1, yearrange[1] + 1)]
print(summers)

x_ = np.arange(0, len(y), 1)
p = np.poly1d(np.polyfit(x_, y, 2))
plt.scatter(x,y, s=0.5)
plt.plot(x, p(x_))
ax = plt.gca()
plt.xlabel('DOY')
plt.ylabel('SNR')
plt.title(r'MIN0 $40^{\circ} - 50^{\circ}$ Average L2 SNR')
ax.set_xlim([x[0], x[-1]])
plt.show()
#plt.savefig('averages.eps', format='eps', dpi=1000)
