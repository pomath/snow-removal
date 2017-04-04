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
        stdev = np.append(stdev, float(tmp[3]))

samp = 1
plt.plot(x[::samp],y[::samp])

plt.plot(x[::samp], (y-stdev)[::samp], '--')
plt.plot(x[::samp], (y+stdev)[::samp], '--')
ax = plt.gca()
plt.xlabel('DOY')
plt.ylabel('SNR')
plt.title(r'MIN0 $40^{\circ} - 50^{\circ}$ Average L2 SNR')
plt.savefig('averages.eps', format='eps', dpi=1000)
