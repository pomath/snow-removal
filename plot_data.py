import matplotlib.pyplot as plt
from array import array
import datetime

x = []
y = array('f')
with open('averages.snr') as f:
    head = f.readline().split()
    startday = datetime.date(int(head[2]),1,int(head[4]))

    for line in f:
        tmp = line.split()
        days2add = 365 * (int(tmp[0]) - startday.year) + int(tmp[1])
        x.append(startday + datetime.timedelta(days2add))
        y.append(float(tmp[2]))

plt.plot(x,y)
ax = plt.gca()
plt.xlabel('DOY')
plt.ylabel('SNR')
plt.title(r'MIN0 $40^{\circ} - 50^{\circ}$ Average L2 SNR')
plt.savefig('averages.png')
